"""
Claude modül 6 · JSON tabanlı özgeçmiş ayrıştırıcı ajan (Claude Agent SDK).

Kavramlar: ajan döngüsü, kendi araçlarınız, allowed_tools, max_turns, durma koşulu,
can_use_tool ile onay. Bölüm 6.2 ve 6.4. TODO'lar sizde.

    python veri/ornek_uret.py
    python ajan.py --ilk 3
    python ajan.py               # tüm klasör

Agent SDK, Claude Code CLI'ını kullanır: https://code.claude.com/docs adresindeki
kurulum adımıyla `claude` komutunun kurulu olduğundan emin olun.
"""
import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
from claude_agent_sdk import (  # noqa: E402
    AssistantMessage, ClaudeAgentOptions, ClaudeSDKClient, ResultMessage, TextBlock, ToolUseBlock,
)

from araclar import SERVER  # noqa: E402
from onay import onay_iste  # noqa: E402

SYSTEM = """Sen bir işe alım asistanısın. Görevin özgeçmiş PDF'lerini Aday şemasına dönüştürmek.

Her dosya için:
1. pdf_oku ile metni oku.
2. Alanları çıkar. Özgeçmişte açıkça yazmayan bir bilgiyi UYDURMA: değeri null bırak ve alan adını eksik listesine yaz.
3. json_dogrula ile doğrula; hata varsa düzeltip tekrar doğrula.
4. kaydet ile kaydet (dosya_adi: PDF'in adı, uzantısız).

TODO 1: Bitiş koşulunu yazın. Örnek: "Verilen dosyaların hepsi işlenince başka araç çağırma;
ad, deneyim yılı ve eksik alanları gösteren bir özet tablo yaz ve bitir."
"""


def yazdir(m) -> None:
    if isinstance(m, AssistantMessage):
        for b in m.content:
            if isinstance(b, ToolUseBlock):
                arg = ", ".join(f"{k}={str(v)[:40]}" for k, v in b.input.items())
                print(f"   → {b.name.removeprefix('mcp__ozgecmis__')}({arg})")
            elif isinstance(b, TextBlock):
                print(b.text)
    elif isinstance(m, ResultMessage):
        print(f"\n[bitti] {m.stop_reason} · maliyet ~{m.total_cost_usd or 0:.4f} USD")


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ilk", type=int, help="yalnız ilk N dosya")
    args = ap.parse_args()

    secenekler = ClaudeAgentOptions(
        model="claude-sonnet-5-5",
        system_prompt=SYSTEM,
        mcp_servers={"ozgecmis": SERVER},
        # TODO 2: İzinsiz çalışacak araçları yazın. kaydet'i buraya KOYMAYIN: onay.py karar versin.
        allowed_tools=[],
        disallowed_tools=["Bash", "Write", "Edit"],      # yerleşik dosya/komut araçları kapalı
        # TODO 3: max_turns verin. Dosya başına kaç tur gerekir? 20 dosya için ne kadar?
        max_turns=None,
        can_use_tool=onay_iste,
    )
    gorev = "Klasördeki özgeçmişleri işle." if not args.ilk else \
        f"dosyalari_listele ile adları al ve yalnız ilk {args.ilk} dosyayı işle."

    async with ClaudeSDKClient(options=secenekler) as ajan:
        await ajan.query(gorev)
        async for m in ajan.receive_response():
            yazdir(m)


if __name__ == "__main__":
    asyncio.run(main())
