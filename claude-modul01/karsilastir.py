"""
Claude modül 1 · Aynı isteği üç modele gönderip süre, token ve maliyeti karşılaştırır.

Kavramlar: model seçimi, usage alanı, token başına fiyat (Bölüm 1.3 ve 1.4).

    python karsilastir.py                      # ornek-log.txt ile
    python karsilastir.py --log baska.log
"""
import argparse
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

# 1M token başına USD: (girdi, çıktı). Güncel fiyat için platform.claude.com/docs → Pricing.
MODELLER = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.0, 10.0),
    "claude-opus-5-5": (4.0, 20.0),
}

GOREV = """Aşağıdaki syslog kayıtlarını bir NOC vardiya notu olarak özetle:
1. Ne oldu (en fazla 3 madde)
2. Etkilenen cihaz ve portlar
3. Kök neden tahmini ve emin olmadığın noktalar
4. Bir sonraki vardiyanın kontrol etmesi gerekenler

<log>
{log}
</log>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--log", default=str(Path(__file__).parent / "ornek-log.txt"))
    args = ap.parse_args()
    log = Path(args.log).read_text(encoding="utf-8")

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY .env dosyasından okunur
    satirlar = []
    for model, (fin, fout) in MODELLER.items():
        t0 = time.perf_counter()
        r = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{"role": "user", "content": GOREV.format(log=log)}],
        )
        sure = time.perf_counter() - t0
        u = r.usage
        maliyet = u.input_tokens / 1e6 * fin + u.output_tokens / 1e6 * fout
        satirlar.append((model, sure, u.input_tokens, u.output_tokens, maliyet))
        metin = "".join(b.text for b in r.content if b.type == "text")
        print(f"\n===== {model} ({r.stop_reason}) =====\n{metin}")

    print(f"\n{'model':<20}{'süre (sn)':>10}{'girdi':>8}{'çıktı':>8}{'maliyet USD':>14}{'1.000 log/gün':>16}")
    for model, sure, i, o, m in satirlar:
        print(f"{model:<20}{sure:>10.1f}{i:>8}{o:>8}{m:>14.5f}{m * 1000:>16.2f}")


if __name__ == "__main__":
    main()
