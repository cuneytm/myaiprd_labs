"""
Claude modül 9 · RAG ile cevap: hibrit arama → en iyi parçalar → Claude (citations).

    python rag/cevapla.py "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import anthropic  # noqa: E402

from ara import yukle  # noqa: E402
from ortak import MODEL, SISTEM, maliyet  # noqa: E402

UST_K = 6


def sor(client: anthropic.Anthropic, indeks, soru: str):
    bulunan = indeks.ara(soru, k=UST_K)
    bloklar = [{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": p["metin"]},
                "title": p["kb"], "context": p["baslik"], "citations": {"enabled": True}} for p in bulunan]
    r = client.messages.create(model=MODEL, max_tokens=800, system=SISTEM,
                               messages=[{"role": "user", "content": bloklar + [{"type": "text", "text": soru}]}])
    return r, bulunan


def main() -> None:
    soru = " ".join(sys.argv[1:]) or "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
    r, bulunan = sor(anthropic.Anthropic(), yukle(), soru)
    print("Bulunan parçalar:", [p["id"] for p in bulunan])
    kaynak = set()
    for b in r.content:
        if b.type == "text":
            print(b.text, end="")
            kaynak |= {c.document_title for c in (b.citations or [])}
    print(f"\n\nKaynaklar (citations): {sorted(kaynak)} · ~{maliyet(r.usage):.4f} USD")


if __name__ == "__main__":
    main()
