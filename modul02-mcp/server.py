"""
Modül 2 laboratuvarı, adım 1: çalışma klasörünü MCP üzerinden sunan bir server.

Modül 1'deki dört dosya fonksiyonu (list_files, read_file, search_files,
write_file) burada aynen duruyor. Tek fark: artık agent'ın kodunda değil, bir
MCP server'da "tool" olarak yayınlanıyorlar. Böylece MCP destekleyen her host
(bu laboratuvardaki agent, MCP Inspector, Claude Desktop, VS Code...) aynı
tool'ları kullanabilir.

MCP'nin üç primitifinin her birinden bir örnek vardır:
    TOOLS     (model kontrollü)    : list_files, read_file, search_files, write_file
    RESOURCES (uygulama kontrollü) : klasor://dosyalar  -> klasördeki bütün dosyaların listesi
    PROMPTS   (kullanıcı kontrollü): ozetle(path)       -> hazır bir istek şablonu

Transport: stdio. Server'ı host alt süreç olarak başlatır; mesajlar stdin/stdout
üzerinden JSON-RPC olarak akar. Bu yüzden print() kullanılmaz: stdout protokole
aittir, log stderr'e yazılır.

Klasör .env'deki WORK_DIR'dan gelir (boşsa depodaki ornek-klasor).
"""

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

REPO = Path(__file__).resolve().parent.parent
load_dotenv(REPO / ".env")
# Göreli bir yol verilirse (ör. "ornek-klasor") depo köküne göre çözülür; komutu hangi klasörden çalıştırdığınız fark etmez.
_wd = Path(os.path.expanduser(os.environ.get("WORK_DIR") or "ornek-klasor"))
WORK_DIR = (_wd if _wd.is_absolute() else REPO / _wd).resolve()
MAX_CHARS = 20_000

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[server] %(message)s")
log = logging.getLogger("klasor")

mcp = MCPServer(
    name="calisma-klasoru",
    instructions=f"'{WORK_DIR.name}' klasöründeki dosyaları listeler, okur, arar ve yazar.",
)


def _path(relative: str) -> Path:
    """Göreli yolu çalışma klasörüne bağlar; klasörün dışına çıkan yolları kabul etmez."""
    p = (WORK_DIR / relative).resolve()
    if p != WORK_DIR and WORK_DIR not in p.parents:
        raise ToolError(f"'{relative}' çalışma klasörünün dışında.")
    return p


# ------------------------------------------------------------------ TOOLS
# Docstring tool'un açıklaması, parametreler JSON Schema'sı olur; SDK ikisini de üretir.

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_files(path: str = ".") -> str:
    """Çalışma klasöründeki (veya bir alt klasöründeki) dosya ve klasörleri listeler. path göreli yoldur; kök için "."."""
    folder = _path(path)
    if not folder.is_dir():
        return f"'{path}' bir klasör değil."
    log.info("list_files %s", path)
    rows = [f"{'[klasör] ' if e.is_dir() else ''}{e.relative_to(WORK_DIR)}"
            for e in sorted(folder.iterdir()) if not e.name.startswith(".")]
    return "\n".join(rows) or "(boş klasör)"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def read_file(path: str) -> str:
    """Bir metin dosyasının içeriğini okur (md, txt, csv, json...). path göreli yoldur, ör. notlar/a.md."""
    f = _path(path)
    if not f.is_file():
        return f"'{path}' bulunamadı."
    log.info("read_file %s", path)
    return f.read_text(encoding="utf-8", errors="replace")[:MAX_CHARS]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def search_files(text: str) -> str:
    """Bütün dosyalarda bir kelime veya ifade arar (büyük/küçük harf duyarsız). Dosya adını bilmediğinde kullan."""
    hits = []
    for f in sorted(WORK_DIR.rglob("*")):
        if f.is_file() and not any(part.startswith(".") for part in f.relative_to(WORK_DIR).parts):
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
            hits += [f"{f.relative_to(WORK_DIR)}:{no}: {line.strip()}"
                     for no, line in enumerate(lines, 1) if text.lower() in line.lower()]
    log.info("search_files %r -> %d eşleşme", text, len(hits))
    return "\n".join(hits[:50]) or "Eşleşme yok."


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
def write_file(path: str, content: str) -> str:
    """Çalışma klasöründe bir dosya oluşturur veya üzerine yazar. Yalnız kullanıcı kaydetmeni istediğinde kullan."""
    f = _path(path)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    log.info("write_file %s (%d karakter)", path, len(content))
    return f"'{path}' kaydedildi ({len(content)} karakter)."


# ------------------------------------------------------------------ RESOURCES

@mcp.resource("klasor://dosyalar", name="dosyalar", description="Çalışma klasöründeki bütün dosyaların listesi",
              mime_type="text/plain")
def dosyalar() -> str:
    return "\n".join(str(f.relative_to(WORK_DIR)) for f in sorted(WORK_DIR.rglob("*"))
                     if f.is_file() and not f.name.startswith("."))


# ------------------------------------------------------------------ PROMPTS

@mcp.prompt(description="Bir dosyayı okuyup kısa bir özet isteyen hazır şablon")
def ozetle(path: str) -> str:
    return f"read_file tool'u ile '{path}' dosyasını oku ve en fazla 5 maddede Türkçe özetle."


if __name__ == "__main__":
    log.info("çalışma klasörü: %s", WORK_DIR)
    mcp.run()  # varsayılan transport: stdio
