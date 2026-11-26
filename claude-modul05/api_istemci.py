"""
Claude modül 5 · Kendi uygulamanızdan MCP server kullanmak.

envanter_server.py'yi alt süreç olarak başlatır (stdio), araçlarını keşfeder (tools/list),
Claude API'nin tool biçimine çevirir ve Claude'un istediği çağrıları server'a iletir (tools/call).

    python api_istemci.py "DC1'de kaç leaf var?"
"""
import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp import Client, StdioServerParameters

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

SERVER = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).parent / "envanter_server.py")])


def metin(sonuc) -> str:
    return "\n".join(getattr(c, "text", "") for c in sonuc.content)


async def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "DC1'de kaç leaf var?"
    claude = anthropic.AsyncAnthropic()
    async with Client(SERVER) as mcp_client:
        araclar = (await mcp_client.list_tools()).tools
        tools = [{"name": t.name, "description": t.description or "", "input_schema": t.input_schema} for t in araclar]
        print("Server'dan gelen araçlar:", ", ".join(t["name"] for t in tools))

        messages = [{"role": "user", "content": soru}]
        for _ in range(8):
            r = await claude.messages.create(model="claude-sonnet-5-5", max_tokens=2048, tools=tools, messages=messages)
            messages.append({"role": "assistant", "content": r.content})
            if r.stop_reason != "tool_use":
                break
            sonuclar = []
            for b in r.content:
                if b.type == "tool_use":
                    print(f"   → {b.name}({b.input})")
                    s = await mcp_client.call_tool(b.name, b.input)
                    sonuclar.append({"type": "tool_result", "tool_use_id": b.id, "content": metin(s),
                                     "is_error": bool(getattr(s, "is_error", False))})
            messages.append({"role": "user", "content": sonuclar})
        print("\n" + "".join(b.text for b in r.content if b.type == "text"))


if __name__ == "__main__":
    asyncio.run(main())
