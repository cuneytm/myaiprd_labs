"""
Claude modül 4 · Files API ve citations: sözleşmeye kaynak gösteren soru-cevap.

Kavramlar: client.files.upload, document bloğunda file_id, citations (sayfa numarası). Bölüm 4.2 ve 4.3.

    python sozlesme_soru.py "Yedek parça teslim süresi nedir?"
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402

KOK = Path(__file__).parent
ID_DOSYASI = KOK / ".sozlesme_file_id"


def file_id(client: anthropic.Anthropic) -> str:
    """Dosyayı bir kez yükler; id'yi saklar ve sonraki çalıştırmalarda yeniden kullanır."""
    if ID_DOSYASI.exists():
        return ID_DOSYASI.read_text().strip()
    f = client.files.upload(file=KOK / "veri" / "sozlesme.pdf")
    ID_DOSYASI.write_text(f.id)
    print("Yüklendi:", f.id)
    return f.id


def main() -> None:
    soru = sys.argv[1] if len(sys.argv) > 1 else "Yedek parça teslim süresi nedir?"
    client = anthropic.Anthropic()
    r = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": [
            {"type": "document", "source": {"type": "file", "file_id": file_id(client)},
             "title": "Bakım ve Destek Sözleşmesi", "citations": {"enabled": True}},
            {"type": "text", "text": soru + " Sözleşmede yazmıyorsa 'sözleşmede yok' de."},
        ]}],
    )
    kaynaklar = []
    for b in r.content:
        if b.type != "text":
            continue
        print(b.text, end="")
        for c in b.citations or []:
            kaynaklar.append(c)
            print(f" [{len(kaynaklar)}]", end="")
    print("\n")
    for i, c in enumerate(kaynaklar, 1):
        sayfa = f"s. {c.start_page_number}" if getattr(c, "start_page_number", None) else ""
        print(f"[{i}] {sayfa}: \"{c.cited_text.strip()[:140]}\"")


if __name__ == "__main__":
    main()
