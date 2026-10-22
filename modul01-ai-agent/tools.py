"""
TOOLS: agent'ın "elleri".

Her tool üç parçadan oluşur:
  1. Python fonksiyonu       -> işi gerçekten yapan kod (harness çalıştırır, model değil)
  2. description             -> modelin tool'u ne zaman kullanacağını anladığı metin
  3. parameters (JSON Schema) -> modelin üretmesi gereken argümanların şekli

Tool'lar .env'deki WORK_DIR klasöründe çalışır. Yollar bu klasöre göre göreli verilir.
Modül 2'de bu dört fonksiyonun aynısını bir MCP server'a taşıyacağız.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")

# Çalışma klasörü: kullanıcının .env'de verdiği klasör, yoksa depodaki örnek klasör
# Göreli bir yol verilirse (ör. "ornek-klasor") depo köküne göre çözülür; komutu hangi klasörden çalıştırdığınız fark etmez.
_wd = Path(os.path.expanduser(os.environ.get("WORK_DIR") or "ornek-klasor"))
WORK_DIR = (_wd if _wd.is_absolute() else REPO / _wd).resolve()
MAX_CHARS = 20_000  # büyük bir dosyanın context'i doldurmaması için


def _path(relative: str) -> Path:
    """Göreli yolu çalışma klasörüne bağlar; klasörün dışına çıkan yolları kabul etmez."""
    p = (WORK_DIR / relative).resolve()
    if p != WORK_DIR and WORK_DIR not in p.parents:
        raise ValueError(f"'{relative}' çalışma klasörünün dışında.")
    return p


# ---------------------------------------------------------------- fonksiyonlar

def list_files(path: str = ".") -> str:
    """Bir klasördeki dosya ve alt klasörleri listeler."""
    folder = _path(path)
    if not folder.is_dir():
        return f"'{path}' bir klasör değil."
    rows = [f"{'[klasör] ' if e.is_dir() else ''}{e.relative_to(WORK_DIR)}"
            for e in sorted(folder.iterdir()) if not e.name.startswith(".")]
    return "\n".join(rows) or "(boş klasör)"


def read_file(path: str) -> str:
    """Bir metin dosyasının içeriğini döndürür."""
    f = _path(path)
    if not f.is_file():
        return f"'{path}' bulunamadı."
    return f.read_text(encoding="utf-8", errors="replace")[:MAX_CHARS]


def search_files(text: str) -> str:
    """Bütün dosyalarda bir metni arar; eşleşen dosya, satır numarası ve satırı döndürür."""
    hits = []
    for f in sorted(WORK_DIR.rglob("*")):
        if f.is_file() and not any(part.startswith(".") for part in f.relative_to(WORK_DIR).parts):
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            hits += [f"{f.relative_to(WORK_DIR)}:{no}: {line.strip()}"
                     for no, line in enumerate(lines, 1) if text.lower() in line.lower()]
    return "\n".join(hits[:50]) or "Eşleşme yok."


def write_file(path: str, content: str) -> str:
    """Bir dosya oluşturur ya da varsa üzerine yazar."""
    f = _path(path)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    return f"'{path}' kaydedildi ({len(content)} karakter)."


# ---------------------------------------------------------------- tool tanımları
# Modele yalnız "description" ve "parameters" gider. "fn" harness'ta kalır.

TOOLS = {
    "list_files": {
        "fn": list_files,
        "description": "Çalışma klasöründeki (veya bir alt klasöründeki) dosya ve klasörleri listeler.",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Göreli klasör yolu; kök için \".\""}},
            "required": [],
        },
    },
    "read_file": {
        "fn": read_file,
        "description": "Bir metin dosyasının içeriğini okur (md, txt, csv, json...).",
        "parameters": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Göreli dosya yolu, ör. notlar/a.md"}},
            "required": ["path"],
        },
    },
    "search_files": {
        "fn": search_files,
        "description": "Bütün dosyalarda bir kelime veya ifade arar (büyük/küçük harf duyarsız). Dosya adını bilmediğinde kullan.",
        "parameters": {
            "type": "object",
            "properties": {"text": {"type": "string", "description": "Aranacak metin"}},
            "required": ["text"],
        },
    },
    "write_file": {
        "fn": write_file,
        "description": "Çalışma klasöründe bir dosya oluşturur veya üzerine yazar. Yalnız kullanıcı kaydetmeni istediğinde kullan.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Göreli dosya yolu, ör. RAPOR.md"},
                "content": {"type": "string", "description": "Dosyanın tam içeriği"},
            },
            "required": ["path", "content"],
        },
    },
}
