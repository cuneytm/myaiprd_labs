"""
Claude modül 6 · Ajanın araçları (Agent SDK @tool, süreç içi MCP server).

Araç adları ajana mcp__ozgecmis__<ad> olarak görünür. Bölüm 6.4.
"""
import json
from pathlib import Path

from claude_agent_sdk import create_sdk_mcp_server, tool
from pydantic import ValidationError
from pypdf import PdfReader

from sema import Aday

KOK = Path(__file__).parent
KAYNAK = KOK / "veri" / "ozgecmisler"
HEDEF = KOK / "adaylar"


def _metin(t: str, hata: bool = False) -> dict:
    sonuc = {"content": [{"type": "text", "text": t}]}
    if hata:
        sonuc["is_error"] = True
    return sonuc


@tool("dosyalari_listele", "İşlenecek özgeçmiş PDF'lerinin adlarını listeler.", {})
async def dosyalari_listele(args: dict) -> dict:
    return _metin("\n".join(sorted(p.name for p in KAYNAK.glob("*.pdf"))))


@tool("pdf_oku", "Bir özgeçmiş PDF'inin metnini döner. dosya: dosyalari_listele'deki ad.", {"dosya": str})
async def pdf_oku(args: dict) -> dict:
    yol = KAYNAK / Path(args["dosya"]).name          # klasör dışına çıkmayı engelle
    if not yol.exists():
        return _metin(f"{args['dosya']} yok. dosyalari_listele ile adları görün.", hata=True)
    return _metin("\n".join(p.extract_text() for p in PdfReader(yol).pages))


@tool("json_dogrula", "Aday JSON'unu şemaya göre doğrular. Kaydetmeden önce MUTLAKA çağır.", {"json": str})
async def json_dogrula(args: dict) -> dict:
    try:
        Aday.model_validate_json(args["json"])
    except ValidationError as e:
        return _metin("Şema hatası:\n" + e.json(include_url=False), hata=True)
    return _metin("Geçerli.")


@tool("kaydet", "Doğrulanmış aday JSON'unu adaylar/<dosya_adi>.json olarak kaydeder.", {"dosya_adi": str, "json": str})
async def kaydet(args: dict) -> dict:
    try:
        aday = Aday.model_validate_json(args["json"])
    except ValidationError:
        return _metin("Geçersiz JSON; önce json_dogrula ile düzeltin.", hata=True)
    HEDEF.mkdir(exist_ok=True)
    ad = Path(args["dosya_adi"]).stem
    (HEDEF / f"{ad}.json").write_text(json.dumps(aday.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    return _metin(f"Kaydedildi: adaylar/{ad}.json")


SERVER = create_sdk_mcp_server(name="ozgecmis", version="1.0.0",
                               tools=[dosyalari_listele, pdf_oku, json_dogrula, kaydet])
