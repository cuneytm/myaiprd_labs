"""
Modül 2 laboratuvarı, adım 2: model OLMADAN bir MCP client.

Bir host'un server'la ne konuştuğunu adım adım gösterir:
  1. server'ı alt süreç olarak başlat ve bağlan (stdio transport)
  2. server'ın neler sunduğunu keşfet: tools/list, resources/list, prompts/list
  3. tool'ları, resource'u ve prompt'u kendimiz çağır

Burada hangi tool'un çağrılacağına KOD karar veriyor. Adım 3'teki agent'ta
(agent_mcp.py) bunu model önerecek.

    python client_test.py
"""

import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

SERVER = StdioServerParameters(command=sys.executable, args=[str(Path(__file__).with_name("server.py"))])


def text_of(result) -> str:
    return "\n".join(getattr(c, "text", str(c)) for c in result.content)


async def main() -> None:
    async with Client(SERVER) as client:
        print("1) Bağlandı.\n")

        print("2a) tools/list")
        for t in (await client.list_tools()).tools:
            print(f"    - {t.name}: {t.description}")
            print(f"      parametreler: {list(t.input_schema.get('properties', {}))}")

        print("\n2b) resources/list")
        for r in (await client.list_resources()).resources:
            print(f"    - {r.uri}: {r.description}")

        print("\n2c) prompts/list")
        for p in (await client.list_prompts()).prompts:
            print(f"    - {p.name}: {p.description}")

        print("\n3a) tools/call list_files(path='.')")
        print(text_of(await client.call_tool("list_files", {"path": "."})))

        print("\n3b) tools/call search_files(text='toplantı')")
        print(text_of(await client.call_tool("search_files", {"text": "toplantı"})))

        print("\n3c) resources/read klasor://dosyalar")
        print((await client.read_resource("klasor://dosyalar")).contents[0].text)

        print("\n3d) prompts/get ozetle(path='yapilacaklar.txt')")
        print((await client.get_prompt("ozetle", {"path": "yapilacaklar.txt"})).messages[0].content.text)


if __name__ == "__main__":
    asyncio.run(main())
