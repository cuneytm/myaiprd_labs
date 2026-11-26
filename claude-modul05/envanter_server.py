"""
Claude modül 5 · Envanter MCP server'ı (stdio).

Kavramlar: MCPServer, @mcp.tool (açıklama docstring'den, şema tiplerden), @mcp.resource,
ToolError ile modele anlamlı hata. Bölüm 5.5. TODO'lar sizde.

Bu dosyayı doğrudan çalıştırmazsınız; bir host başlatır:
    npx @modelcontextprotocol/inspector python envanter_server.py
    claude mcp add envanter -- python /tam/yol/envanter_server.py
    python api_istemci.py "DC1'de kaç leaf var?"
"""
import sys

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from araclar import ENVANTER, config_farki as _config_farki

mcp = MCPServer(
    name="envanter",
    instructions="DC1 ve DC2 fabric envanteri. Salt okunur sorgular.",
)


def log(*a) -> None:
    print("[server]", *a, file=sys.stderr)     # stdout protokole aittir; log stderr'e


@mcp.tool()
def switch_durumu(fabric: str, rol: str = "all") -> str:
    """Bir fabric'teki switch'leri ve config senkron durumlarını listeler. Salt okunurdur.

    Args:
        fabric: Fabric adı, birebir. Örnek: DC1-FABRIC
        rol: all, spine, leaf veya border
    """
    log("switch_durumu", fabric, rol)
    satirlar = [f"{ad}: {d['rol']}, {d['sync']}, NX-OS {d['nxos']}"
                for ad, d in ENVANTER.items()
                if d["fabric"] == fabric and rol in ("all", d["rol"])]
    if not satirlar:
        fabricler = sorted({d["fabric"] for d in ENVANTER.values()})
        raise ToolError(f"{fabric} için kayıt yok. Bilinen fabric'ler: {', '.join(fabricler)}.")
    return "\n".join(satirlar)


# TODO 1: config_farki aracını ekleyin. araclar.config_farki'yi çağırsın; ValueError gelirse
#         mesajını ToolError ile modele iletsin. Docstring'de ne zaman kullanılacağını yazın.


# TODO 2: "envanter://ozet" adresinde bir resource ekleyin: fabric başına cihaz sayısı ve
#         out-of-sync sayısını düz metin olarak dönsün.
#   @mcp.resource("envanter://ozet")
#   def ozet() -> str: ...


if __name__ == "__main__":
    mcp.run()          # transport belirtilmedi: stdio
