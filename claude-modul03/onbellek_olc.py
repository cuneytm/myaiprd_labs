"""
Claude modül 3 · Prompt caching ölçümü.

Aynı runbook'u system prompt'ta taşıyan 5 istek gönderir ve usage alanlarını tabloya yazar.
Kavramlar: cache_control, önek kuralı, cache_creation_input_tokens, cache_read_input_tokens. Bölüm 3.7.

    python onbellek_olc.py
    python onbellek_olc.py --boz      # system prompt'un başına saat ekler: önbellek tutmaz
"""
import argparse
import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

RUNBOOK = (Path(__file__).parent / "veri" / "runbook.md").read_text(encoding="utf-8")
SORULAR = [
    "VLAN adı değişikliği hangi tür değişikliktir?",
    "Border leaf'te route-map değişikliği ne zaman yapılabilir?",
    "VLAN kaldırmadan önce ne kontrol edilir?",
    "Müşteriye VLAN 4000 verilebilir mi?",
    "Acil değişiklik için kimin onayı gerekir?",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boz", action="store_true", help="system prompt'un başına o anki zamanı ekle")
    args = ap.parse_args()
    client = anthropic.Anthropic()

    print(f"{'#':<3}{'girdi':>8}{'cache yazma':>13}{'cache okuma':>13}{'çıktı':>8}")
    for i, soru in enumerate(SORULAR, 1):
        on_ek = f"Şu an: {datetime.datetime.now().isoformat()}\n\n" if args.boz else ""
        r = client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=300,
            system=[{
                "type": "text",
                "text": on_ek + "DC1 runbook'una göre kısa cevap ver.\n\n<runbook>\n" + RUNBOOK + "\n</runbook>",
                "cache_control": {"type": "ephemeral"},   # buraya kadar olan önek önbelleğe alınır
            }],
            messages=[{"role": "user", "content": soru}],
        )
        u = r.usage
        print(f"{i:<3}{u.input_tokens:>8}{u.cache_creation_input_tokens or 0:>13}{u.cache_read_input_tokens or 0:>13}{u.output_tokens:>8}")
    print("\ngirdi: önbellek dışında kalan girdi token'ı. İlk istekte runbook yazılır, sonrakilerde okunmalı.")


if __name__ == "__main__":
    main()
