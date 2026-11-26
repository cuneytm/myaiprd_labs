"""
Claude modül 4 · Topoloji görselinden cihaz ve bağlantı listesi, sonra Mermaid diyagramı.

Kavramlar: image bloğu, görselden yapılandırılmış veri. Bölüm 4.4.

    python topoloji.py veri/topoloji.png
"""
import base64
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
import anthropic  # noqa: E402


class Baglanti(BaseModel):
    a: str
    b: str
    etiket: str | None          # görselde bağlantı üzerinde yazı varsa


class Topoloji(BaseModel):
    cihazlar: list[str]
    baglantilar: list[Baglanti]
    belirsizlikler: list[str]   # emin olunamayan noktalar


def main() -> None:
    yol = Path(sys.argv[1] if len(sys.argv) > 1 else "veri/topoloji.png")
    veri = base64.standard_b64encode(yol.read_bytes()).decode()
    client = anthropic.Anthropic()
    r = client.messages.parse(
        model="claude-sonnet-5-5",
        max_tokens=2048,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": veri}},
            {"type": "text", "text": "Bu ağ topolojisindeki cihazları ve aralarındaki tüm bağlantıları çıkar. "
                                     "Görmediğin bağlantıyı ekleme; emin olmadığın noktaları belirsizliklere yaz."},
        ]}],
        output_format=Topoloji,
    )
    t = r.parsed_output
    print(f"{len(t.cihazlar)} cihaz, {len(t.baglantilar)} bağlantı")
    for b in t.belirsizlikler:
        print("  ? ", b)

    satirlar = ["graph TD"]
    for b in t.baglantilar:
        ok = f" -- {b.etiket} --- " if b.etiket else " --- "
        satirlar.append(f"    {b.a.replace('-', '_')}[{b.a}]{ok}{b.b.replace('-', '_')}[{b.b}]")
    mermaid = "\n".join(satirlar)
    Path("topoloji.mmd").write_text(mermaid, encoding="utf-8")
    print("\n" + mermaid + "\n\nMermaid: topoloji.mmd")


if __name__ == "__main__":
    main()
