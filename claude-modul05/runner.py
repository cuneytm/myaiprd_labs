"""
Claude modül 5 · Aynı iş Tool Runner ile: döngüyü SDK yürütür.

Kavramlar: @beta_tool (açıklama ve şema docstring'den ve tiplerden), tool_runner, until_done(). Bölüm 5.4.

    python runner.py "DC1'de out-of-sync leaf'lerin config farkını göster"
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402
from anthropic import beta_tool  # noqa: E402

import araclar  # noqa: E402


@beta_tool
def switch_durumu(fabric: str, rol: str = "all") -> str:
    """Bir fabric'teki switch'leri ve config senkron durumlarını listeler. Salt okunurdur.

    Args:
        fabric: Fabric adı, birebir. Örnek: DC1-FABRIC
        rol: all, spine, leaf veya border
    """
    return araclar.switch_durumu(fabric, rol)


@beta_tool
def config_farki(cihaz: str) -> str:
    """Bir cihazın beklenen ve çalışan config'i arasındaki farkı unified diff olarak döner.

    Args:
        cihaz: Cihaz adı, birebir. Örnek: LEAF-103
    """
    return araclar.config_farki(cihaz)


def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "DC1'de out-of-sync leaf'lerin config farkını göster"
    client = anthropic.Anthropic()
    runner = client.beta.messages.tool_runner(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        tools=[switch_durumu, config_farki],
        messages=[{"role": "user", "content": soru}],
    )
    for mesaj in runner:                       # her tur bir assistant mesajı
        for b in mesaj.content:
            if b.type == "tool_use":
                print(f"   → {b.name}({b.input})")
    son = runner.until_done()
    print("\n" + "".join(b.text for b in son.content if b.type == "text"))


if __name__ == "__main__":
    main()
