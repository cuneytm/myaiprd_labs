"""
Claude modül 9 · Değerlendirme: uzun bağlam ve RAG'i 25 soruda karşılaştırır.

Ölçütler: doğruluk (beklenen ifade cevapta mı), kaynak isabeti (doğru KB citations'ta mı),
uydurma oranı ("belgede yok" sorularında BILINMIYOR demeyen cevap), toplam maliyet. Bölüm 9.3.

    python eval/calistir.py
    python eval/calistir.py --yontem rag
"""
import argparse
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "rag"))
import anthropic  # noqa: E402

import uzun_baglam  # noqa: E402
from ara import yukle  # noqa: E402
from cevapla import sor as rag_sor  # noqa: E402
from ortak import kb_idleri, maliyet  # noqa: E402


def kaynaklar(r) -> tuple[str, set[str]]:
    metin, k = "", set()
    for b in r.content:
        if b.type == "text":
            metin += b.text
            k |= {c.document_title for c in (b.citations or [])}
    return metin, k | kb_idleri(metin)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yontem", choices=["uzun", "rag", "ikisi"], default="ikisi")
    args = ap.parse_args()
    sorular = [json.loads(s) for s in open(KOK / "eval" / "sorular.jsonl", encoding="utf-8")]
    client = anthropic.Anthropic()
    yontemler = ["uzun", "rag"] if args.yontem == "ikisi" else [args.yontem]
    indeks = yukle() if "rag" in yontemler else None

    tablo = {}
    for y in yontemler:
        dogru = kaynak_ok = olgu = uydurma = yok = 0
        usd = 0.0
        for s in sorular:
            r = uzun_baglam.sor(client, s["soru"]) if y == "uzun" else rag_sor(client, indeks, s["soru"])[0]
            r = r if y == "uzun" else r
            metin, kaynak = kaynaklar(r)
            usd += maliyet(r.usage)
            if s["tur"] == "belgede-yok":
                yok += 1
                ok = "BILINMIYOR" in metin.upper()
                uydurma += not ok
            else:
                olgu += 1
                ok = s["beklenen"].lower() in metin.lower()
                kaynak_ok += s["kaynak"] in kaynak
            dogru += ok
            print(f"[{y}] {s['id']} {'✓' if ok else '✗'}  {metin.strip()[:90]!r}")
        tablo[y] = (dogru, kaynak_ok, olgu, uydurma, yok, usd)

    print(f"\n{'yöntem':<8}{'doğruluk':>10}{'kaynak isabeti':>16}{'uydurma':>10}{'maliyet USD':>14}")
    for y, (d, k, o, u, n, usd) in tablo.items():
        print(f"{y:<8}{d:>7}/{len(sorular)}{k:>13}/{o}{u:>8}/{n}{usd:>14.4f}")


if __name__ == "__main__":
    main()
