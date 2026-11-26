"""
Claude modül 4 · Fatura PDF'inden yapılandırılmış veri.

Kavramlar: document bloğu (base64 PDF), structured outputs, iş kuralı (kalemlerin
toplamı = ara toplam, ara toplam + KDV = genel toplam). Bölüm 4.2 ve 4.5. TODO'lar sizde.

    python fatura.py veri/faturalar/*.pdf
"""
import base64
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402


class Kalem(BaseModel):
    aciklama: str
    miktar: float
    birim_fiyat: float
    tutar: float


class Fatura(BaseModel):
    fatura_no: str
    satici: str
    tarih: str                      # YYYY-AA-GG
    kalemler: list[Kalem]
    ara_toplam: float
    kdv: float
    genel_toplam: float


client = anthropic.Anthropic()


def oku(yol: Path) -> Fatura:
    pdf = base64.standard_b64encode(yol.read_bytes()).decode()
    r = client.messages.parse(
        model="claude-sonnet-5-5",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf}},
                {"type": "text", "text": "Bu faturayı şemaya göre çıkar. Sayıları belgede yazdığı gibi aktar, hesaplayıp düzeltme."},
            ],
        }],
        output_format=Fatura,
    )
    return r.parsed_output


def denetle(f: Fatura) -> list[str]:
    hatalar = []
    # TODO 1: Her kalemde miktar × birim_fiyat ≈ tutar mı? (0,01 TL tolerans)
    # TODO 2: Kalem tutarlarının toplamı ≈ ara_toplam mı?
    # TODO 3: ara_toplam + kdv ≈ genel_toplam mı?
    # Her ihlal için hatalar listesine açıklayıcı bir metin ekleyin.
    return hatalar


def main() -> None:
    for yol in map(Path, sys.argv[1:]):
        f = oku(yol)
        hatalar = denetle(f)
        print(f"\n{yol.name}: {f.fatura_no} · {f.satici} · {f.tarih} · {len(f.kalemler)} kalem · genel toplam {f.genel_toplam:,.2f}")
        print("   " + ("OK" if not hatalar else "KONTROL GEREKLİ: " + "; ".join(hatalar)))


if __name__ == "__main__":
    main()
