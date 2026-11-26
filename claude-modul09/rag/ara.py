"""
Claude modül 9 · Hibrit arama: BM25 (anahtar kelime) + TF-IDF kosinüs (basit vektör).

Bağımlılık yok; amaç mekanizmayı görmek. Gerçek bir sistemde TF-IDF yerine bir embedding modeli
(ör. Voyage AI veya kurum içi bir model) kullanılır: vektor() fonksiyonunu değiştirmek yeterli. Bölüm 9.2.

    python rag/ara.py "jumbo frame MTU"
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent


def kelimeler(t: str) -> list[str]:
    return re.findall(r"[a-zçğıöşü0-9][a-zçğıöşü0-9\-\.]*", t.lower())


class Indeks:
    def __init__(self, parcalar: list[dict]):
        self.p = parcalar
        self.docs = [kelimeler(x["aranan"]) for x in parcalar]
        self.df = Counter(k for d in self.docs for k in set(d))
        self.N = len(self.docs)
        self.ort = sum(map(len, self.docs)) / self.N
        self.vek = [self.vektor(d) for d in self.docs]

    def idf(self, k: str) -> float:
        return math.log(1 + (self.N - self.df[k] + 0.5) / (self.df[k] + 0.5))

    def bm25(self, sorgu: list[str], i: int, k1=1.5, b=0.75) -> float:
        tf, L = Counter(self.docs[i]), len(self.docs[i])
        return sum(self.idf(k) * tf[k] * (k1 + 1) / (tf[k] + k1 * (1 - b + b * L / self.ort)) for k in sorgu if k in tf)

    def vektor(self, d: list[str]) -> dict[str, float]:
        tf = Counter(d)
        v = {k: c * self.idf(k) for k, c in tf.items()}
        n = math.sqrt(sum(x * x for x in v.values())) or 1
        return {k: x / n for k, x in v.items()}

    def ara(self, sorgu: str, k: int = 8) -> list[dict]:
        s = kelimeler(sorgu)
        qv = self.vektor(s)
        bm = [self.bm25(s, i) for i in range(self.N)]
        cos = [sum(qv.get(t, 0) * x for t, x in v.items()) for v in self.vek]
        mb, mc = max(bm) or 1, max(cos) or 1
        skor = [0.5 * bm[i] / mb + 0.5 * cos[i] / mc for i in range(self.N)]      # basit birleştirme
        sira = sorted(range(self.N), key=lambda i: -skor[i])[:k]
        return [{**self.p[i], "skor": round(skor[i], 3)} for i in sira]


def yukle() -> Indeks:
    yol = KOK / "rag" / "indeks.json"
    if not yol.exists():
        sys.exit("Önce indeksi oluşturun: python rag/parcala.py")
    return Indeks(json.loads(yol.read_text(encoding="utf-8")))


if __name__ == "__main__":
    for r in yukle().ara(" ".join(sys.argv[1:]) or "jumbo frame MTU"):
        print(r["skor"], r["id"], r["baslik"])
