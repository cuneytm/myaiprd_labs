"""
Modül 2 laboratuvarı, adım 3: agent + MCP server.

Modül 1'deki agent, dosya tool'larını kendi kodunda (tools.py) tanımlıyordu.
Burada tool'lar MCP server'dan gelir. Agent döngüsü aynı kalır; değişen yalnız
tool'ların nereden geldiği ve nasıl çalıştırıldığıdır:

    1. MCP server'ı başlat ve bağlan              (host -> MCP client -> server)
    2. tools/list ile tool tanımlarını al          (keşif)
    3. tanımları modelin beklediği biçime çevir    (MCP -> OpenAI tool şeması)
    4. döngü: model önerir -> tools/call -> sonuç context'e -> tekrar

    python agent_mcp.py
    python agent_mcp.py --task "Klasörde neler var?"
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import Client, StdioServerParameters
from openai import OpenAI

HERE = Path(__file__).resolve().parent
load_dotenv(HERE.parent / ".env")

llm = OpenAI(base_url=os.environ.get("MODEL_BASE_URL"), api_key=os.environ.get("MODEL_API_KEY", "yok"))
MODEL = os.environ.get("MODEL_NAME")
MAX_STEPS = int(os.environ.get("MAX_STEPS", "10"))

# Host, server'ı alt süreç olarak başlatır (stdio transport)
SERVER = StdioServerParameters(command=sys.executable, args=[str(HERE / "server.py")])

INSTRUCTIONS = (
    "Sen, kullanıcının bilgisayarındaki bir çalışma klasörüyle ilgili işleri yapan bir asistansın. "
    "Klasöre yalnız sana verilen tool'larla erişebilirsin. Bilgiyi tahmin etme, dosyadan oku ve "
    "hangi dosyadan okuduğunu belirt. Dosya oluşturmayı yalnız kullanıcı istediğinde yap. "
    "Cevapların kısa ve Türkçe olsun."
)


def to_openai_tools(mcp_tools) -> list:
    """MCP tool tanımını modelin tool tanımına çevirir. İçerik aynıdır: ad, açıklama, JSON Schema."""
    return [{"type": "function",
             "function": {"name": t.name, "description": t.description or "", "parameters": t.input_schema}}
            for t in mcp_tools]


async def run_task(client: Client, specs: list, messages: list) -> str:
    for step in range(1, MAX_STEPS + 1):
        msg = llm.chat.completions.create(model=MODEL, messages=messages, tools=specs).choices[0].message
        if not msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or ""})
            return msg.content or ""

        messages.append({
            "role": "assistant", "content": msg.content or "",
            "tool_calls": [{"id": c.id, "type": "function",
                            "function": {"name": c.function.name, "arguments": c.function.arguments}}
                           for c in msg.tool_calls],
        })
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print(f"  [adım {step} · MCP tools/call] {call.function.name}({json.dumps(args, ensure_ascii=False)})")
            r = await client.call_tool(call.function.name, args)          # MCP üzerinden çalıştır
            result = "\n".join(getattr(c, "text", str(c)) for c in r.content)
            print(f"  [adım {step} · sonuç] {result.replace(chr(10), ' | ')[:150]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
    return f"{MAX_STEPS} adımda bitmedi; görev durduruldu."


async def main(task: str | None) -> None:
    async with Client(SERVER) as client:                     # 1. bağlan
        tools = (await client.list_tools()).tools            # 2. keşif
        specs = to_openai_tools(tools)                        # 3. çeviri
        print(f"Model: {MODEL}  ·  MCP server'dan {len(tools)} tool alındı: {', '.join(t.name for t in tools)}")

        messages = [{"role": "system", "content": INSTRUCTIONS}]
        if task:
            messages.append({"role": "user", "content": task})
            print(await run_task(client, specs, messages))
            return
        print("Çıkmak için: q\n")
        while True:                                           # 4. döngü
            text = input("Siz> ").strip()
            if text.lower() in ("q", "quit", "exit", "çık"):
                break
            if text:
                messages.append({"role": "user", "content": text})
                print(f"\nAgent> {await run_task(client, specs, messages)}\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Modül 2: agent + MCP server")
    p.add_argument("--task", help="Tek bir görev çalıştır ve çık")
    try:
        asyncio.run(main(p.parse_args().task))
    except KeyboardInterrupt:
        pass
