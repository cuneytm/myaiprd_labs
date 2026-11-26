"""
Claude modül 8 · Kurgusal mağaza MCP server'ı (stdio).

Araçlar: siparis_getir, urun_ara (salt okunur), iade_baslat (yazma, geri alınamaz).
Her çağrı islem_log.jsonl'e yazılır; degerlendir.py davranışı buradan kontrol eder. Bölüm 5.5 ve 8.

    npx @modelcontextprotocol/inspector python magaza_server.py
"""
import datetime
import json
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

KOK = Path(__file__).parent
SIPARISLER = {s["siparis_no"]: s for s in json.loads((KOK / "veri" / "siparisler.json").read_text(encoding="utf-8"))}
URUNLER = json.loads((KOK / "veri" / "urunler.json").read_text(encoding="utf-8"))
MUSTERILER = json.loads((KOK / "veri" / "musteriler.json").read_text(encoding="utf-8"))
LOG = KOK / "islem_log.jsonl"
BUGUN = datetime.date(2026, 11, 26)          # veriler bu tarihe göre üretildi

mcp = MCPServer(name="magaza", instructions="Kurgusal mağaza: sipariş, ürün ve iade işlemleri.")


def kayit(arac: str, girdi: dict, sonuc: str, hata: bool = False) -> None:
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"zaman": datetime.datetime.now().isoformat(), "arac": arac, "girdi": girdi,
                            "hata": hata, "sonuc": sonuc[:300]}, ensure_ascii=False) + "\n")
    print(f"[server] {arac} {girdi} {'HATA' if hata else ''}", file=sys.stderr)


@mcp.tool()
def siparis_getir(siparis_no: str) -> str:
    """Bir siparişin durumunu, tarihini, tutarını, kalemlerini ve kargo takip numarasını döner. Salt okunur.

    Args:
        siparis_no: Sipariş numarası, ör. SP-1042
    """
    s = SIPARISLER.get(siparis_no.strip().upper())
    if not s:
        kayit("siparis_getir", {"siparis_no": siparis_no}, "yok", True)
        raise ToolError(f"{siparis_no} bulunamadı. Sipariş numarası SP-1030 ile SP-1079 arasında olmalı.")
    m = MUSTERILER[s["musteri"]]
    kalemler = [next(u["ad"] for u in URUNLER if u["sku"] == k) for k in s["kalemler"]]
    gun = (BUGUN - datetime.date.fromisoformat(s["tarih"])).days
    metin = (f"{s['siparis_no']} · {s['tarih']} ({gun} gün önce) · {s['durum']} · {s['tutar']:.2f} TL\n"
             f"Kalemler: {', '.join(kalemler)}\nKargo: {s['kargo_takip'] or '-'}\n"
             f"Müşteri: {m['ad']} (iletişim bilgileri maskeli)")
    kayit("siparis_getir", {"siparis_no": siparis_no}, metin)
    return metin


@mcp.tool()
def urun_ara(sorgu: str) -> str:
    """Ürün kataloğunda ad veya kategoriye göre arar; fiyat, stok ve uyumluluk bilgisini döner. Salt okunur.

    Args:
        sorgu: Aranacak kelimeler, ör. "kablosuz kulaklık" veya "65W"
    """
    kelimeler = sorgu.lower().split()
    bulunan = [u for u in URUNLER if all(k in (u["ad"] + " " + u["kategori"]).lower() for k in kelimeler)][:8]
    if not bulunan:
        kayit("urun_ara", {"sorgu": sorgu}, "yok")
        return f"'{sorgu}' için ürün bulunamadı. Daha az kelimeyle arayın."
    metin = "\n".join(f"{u['sku']} · {u['ad']} · {u['fiyat']:.2f} TL · stok {u['stok']} · uyumlu: {', '.join(u['uyumluluk'])}"
                      for u in bulunan)
    kayit("urun_ara", {"sorgu": sorgu}, metin)
    return metin


@mcp.tool()
def iade_baslat(siparis_no: str, tutar: float, neden: str) -> str:
    """Bir sipariş için iade başlatır ve ödemeyi geri gönderir. GERİ ALINAMAZ.

    Args:
        siparis_no: Sipariş numarası
        tutar: İade edilecek tutar (TL)
        neden: Müşterinin belirttiği iade nedeni
    """
    girdi = {"siparis_no": siparis_no, "tutar": tutar, "neden": neden}
    s = SIPARISLER.get(siparis_no.strip().upper())
    if not s:
        kayit("iade_baslat", girdi, "yok", True)
        raise ToolError(f"{siparis_no} bulunamadı.")
    # Alıştırma: buraya iki kod kontrolü ekleyin (tutar ≤ sipariş tutarı, sipariş en fazla 30 günlük).
    metin = f"İade başlatıldı: {s['siparis_no']}, {tutar:.2f} TL. İade no: IA-{abs(hash((siparis_no, tutar))) % 100000:05d}"
    kayit("iade_baslat", girdi, metin)
    return metin


if __name__ == "__main__":
    mcp.run()
