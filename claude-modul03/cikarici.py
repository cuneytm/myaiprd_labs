"""
Claude modül 3 · Değişiklik talebi çıkarıcı.

Kavramlar: structured outputs (messages.parse), iş kuralı doğrulaması,
hatayı geri bildirerek yeniden deneme, insana yönlendirme. Bölüm 3.4 ve 3.5.

    python cikarici.py veri/talepler.jsonl --ilk 10
"""
import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

from sema import DegisiklikTalebi  # noqa: E402

MODEL = "claude-sonnet-5-5"
RUNBOOK = (Path(__file__).parent / "veri" / "runbook.md").read_text(encoding="utf-8")
SYSTEM = (
    "Değişiklik taleplerini DC1 runbook'una göre analiz eden bir network mühendisisin. "
    "Talepte olmayan bilgiyi uydurma.\n\n<runbook>\n" + RUNBOOK + "\n</runbook>"
)
MAKS_DENEME = 2

client = anthropic.Anthropic()


def kurallari_denetle(t: DegisiklikTalebi) -> list[str]:
    """İş kuralları: şema biçimi garanti eder, anlamı biz kontrol ederiz."""
    hatalar: list[str] = []
    # TODO 1: VLAN kurallarını ekleyin (runbook bölüm 5):
    #   - vlan_id 1-4094 aralığında olmalı
    #   - müşteri VLAN'ı 100-3966 aralığında olmalı (rezerve aralıklar müşteriye verilmez)
    #   Her ihlal için açıklayıcı bir metin ekleyin, ör. f"vlan_id {t.vlan_id} 1-4094 dışında"
    if t.risk == "yuksek" and not t.bakim_penceresi_gerekli:
        hatalar.append("risk 'yuksek' ama bakım penceresi gerekli değil denmiş; runbook'a göre yüksek risk pencere ister")
    return hatalar


def talep_cikar(metin: str) -> tuple[DegisiklikTalebi | None, list[str], int]:
    """(talep, kalan_hatalar, deneme_sayisi) döner. Kalan hata varsa talep insana gider."""
    mesajlar = [{"role": "user", "content": metin}]
    for deneme in range(1, MAKS_DENEME + 1):
        r = client.messages.parse(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM,
            messages=mesajlar,
            output_format=DegisiklikTalebi,
        )
        if r.stop_reason == "max_tokens":
            raise RuntimeError("Çıktı yarım kaldı; max_tokens'ı artırın.")
        t = r.parsed_output
        hatalar = kurallari_denetle(t)
        if not hatalar:
            return t, [], deneme
        # TODO 2: Hatayı Claude'a açıkça geri verin ve tekrar isteyin. Örnek:
        #   mesajlar += [
        #       {"role": "assistant", "content": t.model_dump_json()},
        #       {"role": "user", "content": "Bu çıktıda şu sorunlar var: " + "; ".join(hatalar)
        #                                   + ". Talebi yeniden değerlendir. VLAN numarası talepte geçersizse değiştirme, özetinde belirt."},
        #   ]
        # Şimdilik yeniden denemeden çıkıyoruz:
        return t, hatalar, deneme
    return t, hatalar, MAKS_DENEME


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dosya")
    ap.add_argument("--ilk", type=int, default=10)
    args = ap.parse_args()

    insana = 0
    with open(args.dosya, encoding="utf-8") as f:
        talepler = [json.loads(s) for s in f][: args.ilk]
    for d in talepler:
        t, hatalar, deneme = talep_cikar(d["metin"])
        durum = "İNSANA" if hatalar else "OK"
        insana += bool(hatalar)
        print(f"\n{d['id']} [{durum}, {deneme} deneme]  {d['metin'][:80]}...")
        print("  ", t.model_dump_json())
        for h in hatalar:
            print("   ! ", h)
    print(f"\n{len(talepler)} talep, {insana} tanesi insan incelemesine gitti.")


if __name__ == "__main__":
    main()
