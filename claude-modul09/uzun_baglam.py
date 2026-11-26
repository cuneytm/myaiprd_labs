"""
Claude modül 9 · Uzun bağlam: 40 runbook'un tamamı bağlamda, prompt caching ve citations ile.

Kavramlar: çok sayıda document bloğu, cache_control (son belgeye kadar önek önbellekte),
citations, usage'da cache alanları. Bölüm 9.1 ve 4.3.

    python uzun_baglam.py "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
"""
import sys

import anthropic

from ortak import MODEL, SISTEM, maliyet, runbooklar


def belgeler() -> list[dict]:
    bloklar = [{"type": "document", "source": {"type": "text", "media_type": "text/plain", "data": metin},
                "title": kb, "citations": {"enabled": True}} for kb, metin in runbooklar()]
    bloklar[-1]["cache_control"] = {"type": "ephemeral"}      # 40 belgenin tamamı önbelleğe
    return bloklar


def sor(client: anthropic.Anthropic, soru: str):
    return client.messages.create(
        model=MODEL, max_tokens=800, system=SISTEM,
        messages=[{"role": "user", "content": belgeler() + [{"type": "text", "text": soru}]}],
    )


def cevap_ve_kaynaklar(r) -> tuple[str, set[str]]:
    metin, kaynak = "", set()
    for b in r.content:
        if b.type == "text":
            metin += b.text
            for c in b.citations or []:
                kaynak.add(c.document_title)
    return metin, kaynak


def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "BGP komşusu Idle durumunda kalıyorsa ilk ne kontrol edilir?"
    client = anthropic.Anthropic()
    r = sor(client, soru)
    metin, kaynak = cevap_ve_kaynaklar(r)
    u = r.usage
    print(metin)
    print(f"\nKaynaklar (citations): {sorted(kaynak)}")
    print(f"usage: girdi {u.input_tokens} · cache yazma {u.cache_creation_input_tokens} · "
          f"cache okuma {u.cache_read_input_tokens} · çıktı {u.output_tokens} · ~{maliyet(u):.4f} USD")
    print("İkinci kez çalıştırın: cache okuma dolmalı, maliyet düşmeli.")


if __name__ == "__main__":
    main()
