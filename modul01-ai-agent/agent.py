"""
Modül 1 laboratuvarı: basit bir AI agent.

    agent = model + harness
    harness = instructions + tools + skills + memory + loop

Bu dosya HARNESS'tır: modelin dışındaki yazılım. Model yalnız bir sonraki adımı
ÖNERİR ("şu tool'u şu argümanla çağır" ya da "cevap şu"). Tool'u çalıştıran,
hatırlayan ve döngüyü yöneten bu dosyadır.

Dosya, sunumdaki parçalara göre bölümlere ayrılmıştır.

Çalıştırma (ayrıntı: HOWTO.md):
    python agent.py                     # sohbet
    python agent.py --task "..."        # tek görev
    python agent.py --tasks tasks.txt   # dış döngü: görev kuyruğu
    python agent.py --resume            # önceki sohbete devam
"""

import argparse
import datetime
import json
import os
import re
from pathlib import Path

from openai import OpenAI

from tools import TOOLS, WORK_DIR  # tools.py, .env dosyasını da yükler

HERE = Path(__file__).resolve().parent

# =====================================================================
# MODEL: adres, ad ve anahtar .env dosyasından gelir
# =====================================================================
client = OpenAI(
    base_url=os.environ.get("MODEL_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.environ.get("MODEL_API_KEY", "yok"),
)
MODEL = os.environ.get("MODEL_NAME", "qwen3:8b")
MAX_STEPS = int(os.environ.get("MAX_STEPS", "10"))


# =====================================================================
# INSTRUCTIONS: sabit rol ve kurallar; her model çağrısında context'in başına konur.
# TASK ise her seferinde değişir: kullanıcının mesajı ya da kuyruktan gelen iş.
# =====================================================================
INSTRUCTIONS = (HERE / "instructions.md").read_text(encoding="utf-8")


# =====================================================================
# SKILLS: paketlenmiş prosedür. Context'e yalnız ad + açıklama (katalog) konur;
# gövdeyi model gerektiğinde load_skill tool'u ile kendisi ister.
# =====================================================================
def read_skills() -> dict:
    skills = {}
    for f in sorted((HERE / "skills").glob("*/SKILL.md")):
        text = f.read_text(encoding="utf-8")
        meta = dict(re.findall(r"^(name|description):\s*(.+)$", text, re.M))
        skills[meta["name"]] = {"description": meta["description"], "body": text.split("---", 2)[-1].strip()}
    return skills


SKILLS = read_skills()


def load_skill(name: str) -> str:
    return SKILLS[name]["body"] if name in SKILLS else f"'{name}' adında skill yok. Mevcut: {', '.join(SKILLS)}"


# =====================================================================
# MEMORY: model durumsuzdur, hatırlayan harness'tır.
#   short-term : bu görevin mesajları (messages listesi = context)
#   session    : sohbet dosyaya kaydedilir, --resume ile geri yüklenir
#   long-term  : kalıcı bilgiler (memory/facts.md), her görevde context'e konur
#   procedural : skill'ler (yukarıda)
# =====================================================================
MEMORY_DIR = HERE / "memory"
FACTS_FILE = MEMORY_DIR / "facts.md"
SESSION_FILE = MEMORY_DIR / "session.json"


def remember(fact: str) -> str:
    MEMORY_DIR.mkdir(exist_ok=True)
    with FACTS_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {fact}\n")
    return "Kaydedildi."


def save_session(messages: list) -> None:
    MEMORY_DIR.mkdir(exist_ok=True)
    SESSION_FILE.write_text(json.dumps(messages, ensure_ascii=False, indent=1), encoding="utf-8")


def system_prompt() -> str:
    """Context'in sabit kısmı: instructions + skill kataloğu + uzun dönem bellek."""
    catalog = "\n".join(f"- {n}: {s['description']}" for n, s in SKILLS.items())
    facts = FACTS_FILE.read_text(encoding="utf-8") if FACTS_FILE.exists() else "(henüz yok)"
    return (
        f"{INSTRUCTIONS}\n\n"
        f"## Kullanılabilir skill'ler (gövdesini load_skill ile oku)\n{catalog}\n\n"
        f"## Kullanıcı hakkında bildiklerin (uzun dönem bellek)\n{facts}"
    )


# =====================================================================
# TOOLS: tools.py'deki dosya tool'ları + harness'ın kendi tool'ları (skill ve bellek).
# Modele yalnız tanım (ad, açıklama, şema) gider; fonksiyonu harness çalıştırır.
# =====================================================================
ALL_TOOLS = dict(TOOLS)
ALL_TOOLS["load_skill"] = {
    "fn": load_skill,
    "description": "Bir skill'in tam talimatını getirir. Katalogdaki bir skill'e uyan bir işe başlamadan önce çağır.",
    "parameters": {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]},
}
ALL_TOOLS["remember"] = {
    "fn": remember,
    "description": "Kullanıcının verdiği kalıcı bir bilgiyi veya tercihi uzun dönem belleğe kaydeder (tek cümle).",
    "parameters": {"type": "object", "properties": {"fact": {"type": "string"}}, "required": ["fact"]},
}

TOOL_SPECS = [
    {"type": "function", "function": {"name": n, "description": t["description"], "parameters": t["parameters"]}}
    for n, t in ALL_TOOLS.items()
]


def run_tool(name: str, raw_args: str) -> str:
    """Modelin önerdiği tool'u çalıştırır ve sonucu metin olarak döndürür."""
    try:
        return ALL_TOOLS[name]["fn"](**json.loads(raw_args or "{}"))
    except Exception as e:  # hata da bir sonuçtur: model okuyup düzeltebilir
        return f"HATA: {e}"


# =====================================================================
# LOOP (iç döngü, ReAct): modeli çağır -> tool önerdiyse çalıştır -> sonucu
# context'e ekle -> tekrar. Model tool önermeden cevap verince durur.
# MAX_STEPS, döngünün sonsuza kadar sürmemesi için bir üst sınırdır.
# =====================================================================
def run_task(messages: list) -> str:
    for step in range(1, MAX_STEPS + 1):
        msg = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOL_SPECS).choices[0].message

        if not msg.tool_calls:                                  # tool yok: final cevap
            messages.append({"role": "assistant", "content": msg.content or ""})
            return msg.content or ""

        # Modelin önerisini context'e ekle: bir sonraki adımda ne istediğini görmeli
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [{"id": c.id, "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments}}
                           for c in msg.tool_calls],
        })
        for call in msg.tool_calls:
            print(f"  [adım {step} · model önerdi] {call.function.name}({call.function.arguments})")
            result = run_tool(call.function.name, call.function.arguments)
            print(f"  [adım {step} · sonuç] {result.replace(chr(10), ' | ')[:150]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return f"{MAX_STEPS} adımda bitmedi; görev durduruldu."


def new_context() -> list:
    return [{"role": "system", "content": system_prompt()}]


# =====================================================================
# GÖREV NEREDEN GELİR: sohbet, tek görev ve görev kuyruğu (dış döngü)
# =====================================================================
def chat(resume: bool) -> None:
    """Sohbet: her adımı kullanıcı başlatır; mesajlar aynı context'te birikir."""
    if resume and SESSION_FILE.exists():
        messages = json.loads(SESSION_FILE.read_text(encoding="utf-8"))
        messages[0] = new_context()[0]   # instructions ve bellek güncel haliyle
        print(f"Önceki oturum yüklendi ({len(messages)} mesaj).")
    else:
        messages = new_context()
    print("Çıkmak için: q\n")
    while True:
        task = input("Siz> ").strip()
        if task.lower() in ("q", "quit", "exit", "çık"):
            break
        if task:
            messages.append({"role": "user", "content": task})
            print(f"\nAgent> {run_task(messages)}\n")
            save_session(messages)


def run_queue(path: str) -> None:
    """Dış döngü: kuyruktaki her görev ayrı bir iç döngüde, temiz bir context ile çalışır."""
    tasks = [t.strip() for t in Path(path).read_text(encoding="utf-8").splitlines()
             if t.strip() and not t.startswith("#")]
    results = []
    for i, task in enumerate(tasks, 1):
        print(f"\n=== Görev {i}/{len(tasks)}: {task}")
        answer = run_task(new_context() + [{"role": "user", "content": task}])
        print(f"--> {answer}")
        results.append(f"## {task}\n\n{answer}\n")
    out = MEMORY_DIR / f"kuyruk-{datetime.datetime.now():%Y%m%d-%H%M}.md"
    MEMORY_DIR.mkdir(exist_ok=True)
    out.write_text("\n".join(results), encoding="utf-8")
    print(f"\nSonuçlar: {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Modül 1: basit AI agent")
    p.add_argument("--task", help="Tek bir görev çalıştır ve çık")
    p.add_argument("--tasks", help="Görev kuyruğu dosyası (dış döngü)")
    p.add_argument("--resume", action="store_true", help="Önceki sohbet oturumunu yükle")
    a = p.parse_args()

    print(f"Model: {MODEL}  ·  Klasör: {WORK_DIR}")
    try:
        if a.task:
            print(run_task(new_context() + [{"role": "user", "content": a.task}]))
        elif a.tasks:
            run_queue(a.tasks)
        else:
            chat(a.resume)
    except KeyboardInterrupt:
        pass
