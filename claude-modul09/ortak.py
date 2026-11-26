"""Claude modül 9 · Ortak yardımcılar: runbook'ları yüklemek ve maliyet hesabı."""
import re
from pathlib import Path

from dotenv import load_dotenv

KOK = Path(__file__).parent
load_dotenv(KOK.parent / ".env")

MODEL = "claude-sonnet-5-5"
FIYAT = {"girdi": 2.0, "cikti": 10.0, "cache_yazma": 2.5, "cache_okuma": 0.10}   # USD / 1M token (Sonnet 5.5)


def runbooklar() -> list[tuple[str, str]]:
    """[(KB-101, metin), ...]"""
    return [(p.stem, p.read_text(encoding="utf-8")) for p in sorted((KOK / "runbooklar").glob("KB-*.md"))]


def maliyet(u) -> float:
    return (u.input_tokens * FIYAT["girdi"] + u.output_tokens * FIYAT["cikti"]
            + (u.cache_creation_input_tokens or 0) * FIYAT["cache_yazma"]
            + (u.cache_read_input_tokens or 0) * FIYAT["cache_okuma"]) / 1e6


def kb_idleri(metin: str) -> set[str]:
    return set(re.findall(r"KB-\d{3}", metin))


SISTEM = ("Sen DC1 network runbook asistanısın. Yalnız verilen runbook'lara dayanarak cevap ver. "
          "Cevap runbook'larda yoksa yalnızca 'BILINMIYOR' yaz ve hangi ekibe sorulabileceğini söyleme. "
          "Cevabının sonunda dayandığın runbook kimliklerini [KB-xxx] biçiminde yaz.")
