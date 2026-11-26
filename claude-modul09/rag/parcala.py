"""
Claude modül 9 · Runbook'ları başlıklara göre parçalar ve indeks dosyası yazar (rag/indeks.json).

Kavramlar: başlığa göre parçalama, contextual retrieval (her parçaya dokümandaki yerini anlatan
kısa bağlam, Haiku + prompt caching ile). Bölüm 9.2. TODO sizde.

    python rag/parcala.py              # bağlamsız
    python rag/parcala.py --baglam     # contextual retrieval (TODO tamamlandıktan sonra)
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import anthropic  # noqa: E402

from ortak import KOK, runbooklar  # noqa: E402

BAGLAM_PROMPT = """Aşağıdaki parçanın yukarıdaki dokümanın neresinde olduğunu ve ne hakkında olduğunu
1-2 cümleyle açıkla. Yalnız açıklamayı yaz.
<parca>{parca}</parca>"""


def parcala(kb: str, metin: str) -> list[dict]:
    baslik = metin.splitlines()[0].lstrip("# ").strip()
    bolumler = re.split(r"\n(?=## )", metin)
    return [{"id": f"{kb}#{i}", "kb": kb, "baslik": baslik, "metin": b.strip()} for i, b in enumerate(bolumler[1:], 1)]


def baglam_ekle(client: anthropic.Anthropic, dokuman: str, parca: str) -> str:
    # TODO: Bölüm 9.2'deki örneği uygulayın.
    #  - model: claude-haiku-5-5, max_tokens ~150
    #  - Dokümanı system'e (veya mesajın başına) koyun ve cache_control ile işaretleyin: aynı dokümanın
    #    tüm parçaları için doküman önbellekten okunur, yalnız parça ücretlendirilir.
    #  - Dönüş: Claude'un açıklaması + "\n\n" + parca
    return parca


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baglam", action="store_true")
    args = ap.parse_args()
    client = anthropic.Anthropic() if args.baglam else None
    parcalar = []
    for kb, metin in runbooklar():
        for p in parcala(kb, metin):
            p["aranan"] = baglam_ekle(client, metin, p["metin"]) if args.baglam else f"{p['baslik']}\n{p['metin']}"
            parcalar.append(p)
        print(".", end="", flush=True)
    yol = KOK / "rag" / "indeks.json"
    yol.write_text(json.dumps(parcalar, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(parcalar)} parça → {yol}")


if __name__ == "__main__":
    main()
