"""
Claude modül 5 · Elle yazılmış tool use döngüsü.

Kavramlar: tools listesi, stop_reason "tool_use", tool_use / tool_result blokları,
is_error, paralel çağrıların sonuçlarını tek mesajda göndermek. Bölüm 5.1. TODO'lar sizde.

    python dongu.py "DC1'de out-of-sync leaf'lerin config farkını göster"
"""
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

from araclar import ARACLAR, TOOLS  # noqa: E402

MAKS_TUR = 8


def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "DC1'de out-of-sync leaf'lerin config farkını göster"
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": soru}]

    for tur in range(1, MAKS_TUR + 1):
        r = client.messages.create(model="claude-sonnet-5-5", max_tokens=4096, tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": r.content})       # cevabı olduğu gibi geçmişe ekle
        if r.stop_reason != "tool_use":
            break

        cagrilar = [b for b in r.content if b.type == "tool_use"]
        print(f"\n[tur {tur}] {len(cagrilar)} araç çağrısı" + (" (paralel)" if len(cagrilar) > 1 else ""))
        sonuclar = []
        for blok in cagrilar:
            print(f"   → {blok.name}({json.dumps(blok.input, ensure_ascii=False)})")
            # TODO 1: Aracı çalıştırın: cikti = ARACLAR[blok.name](**blok.input)
            #         ve sonuclar'a {"type": "tool_result", "tool_use_id": blok.id, "content": cikti} ekleyin.
            # TODO 2: Araç istisna fırlatırsa sonucu ATLAMAYIN: aynı tool_use_id ile
            #         {"type": "tool_result", "tool_use_id": blok.id, "content": f"Hata: {e}", "is_error": True} ekleyin.
            pass
        # TODO 3: Tüm sonuçları TEK bir user mesajında gönderin:
        #         messages.append({"role": "user", "content": sonuclar})
        #         (Her tool_use'a bir tool_result yoksa sonraki istek 400 döner.)
    else:
        print(f"\n[{MAKS_TUR} turda bitmedi, durduruldu]")

    print("\n" + "".join(b.text for b in r.content if b.type == "text"))


if __name__ == "__main__":
    main()
