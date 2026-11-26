"""
Claude modül 2 · Terminalde log açıklayan asistan.

Kavramlar: çok turlu konuşma (geçmişi her istekte göndermek), streaming, hata yakalama.
Bölüm 2.5, 2.6 ve 2.7. Üç TODO sizde.

    python asistan.py --log ornek-loglar/bgp-flap.log
    (çıkmak için boş satır veya Ctrl+C)
"""
import argparse
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

MODEL = "claude-sonnet-5-5"
SYSTEM = (
    "Sen bir network operasyon asistanısın. Kullanıcı sana bir log verir ve sorular sorar. "
    "Yalnız logda görünenlere dayan; logda olmayan bir şeyi tahmin ediyorsan 'tahmin' diye belirt. Türkçe ve kısa yaz."
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", required=True)
    args = ap.parse_args()
    log = Path(args.log).read_text(encoding="utf-8")

    client = anthropic.Anthropic()
    gecmis: list[dict] = []
    ilk = True

    while True:
        try:
            soru = input("\nsoru> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not soru:
            break
        icerik = f"<log>\n{log}\n</log>\n\n{soru}" if ilk else soru
        ilk = False
        gecmis.append({"role": "user", "content": icerik})

        try:
            # TODO 2: Cevabı streaming ile, geldikçe yazdırın.
            #   with client.messages.stream(model=..., max_tokens=..., system=..., messages=gecmis) as s:
            #       for parca in s.text_stream: print(parca, end="", flush=True)
            #       r = s.get_final_message()
            # Şimdilik cevap tek parça geliyor:
            r = client.messages.create(model=MODEL, max_tokens=1024, system=SYSTEM, messages=gecmis)
            metin = "".join(b.text for b in r.content if b.type == "text")
            print(metin)
        # TODO 3: anthropic.RateLimitError'u yakalayın; kullanıcıya "biraz bekleyip tekrar deneyin" deyin
        #         ve son user mesajını gecmis'ten çıkarın ki konuşma bozulmasın.
        except anthropic.APIStatusError as e:
            print(f"\n[API hatası {e.status_code}] {e.message}")
            gecmis.pop()
            continue

        # TODO 1: Claude'un cevabını geçmişe ekleyin. Eklemezseniz ikinci soruda Claude
        #         ilk cevabını "hatırlamaz" ve API art arda iki user mesajı görür.
        #   gecmis.append({"role": "assistant", "content": r.content})

        print(f"\n[usage] girdi {r.usage.input_tokens} · çıktı {r.usage.output_tokens} · stop_reason {r.stop_reason}")


if __name__ == "__main__":
    main()
