"""
Claude modül 4 · Örnek dosyaları üretir (kurgusal):
  veri/faturalar/fatura-1.pdf ... fatura-5.pdf   (fatura-4'te genel toplam bilerek yanlış)
  veri/topoloji.png                               (küçük bir leaf-spine topolojisi)
  veri/sozlesme.pdf                               (4 sayfalık bakım-destek sözleşmesi)

    python veri/ornek_uret.py

Not: fpdf2'nin yerleşik fontları Türkçe karakterleri içermediği için PDF metinleri
Türkçe karakterler sadeleştirilerek yazılır (ş→s, ğ→g ...). Claude bunu sorunsuz okur.
"""
from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw

KOK = Path(__file__).parent
SADE = str.maketrans("şŞğĞıİçÇöÖüÜ", "sSgGiIcCoOuU")


def s(t: str) -> str:
    return t.translate(SADE)


FATURALAR = [
    ("FT-2026-0412", "Kuzey Ag Teknolojileri", "2026-10-03", [("100G QSFP28 SR4 modul", 8, 2150.0), ("25G SFP28 DAC 3m", 24, 310.0), ("Kurulum hizmeti (gun)", 2, 9500.0)]),
    ("FT-2026-0419", "Deniz Sistem Entegrasyon", "2026-10-09", [("Leaf switch 48x25G + 6x100G", 2, 412000.0), ("Yillik destek paketi", 2, 38500.0)]),
    ("FT-2026-0431", "Atlas Kablo", "2026-10-15", [("OM4 MPO-12 patch 5m", 40, 640.0), ("Fiber kaset 24 port", 6, 2875.0)]),
    ("FT-2026-0447", "Orion Guvenlik", "2026-10-22", [("Firewall lisans yenileme (1 yil)", 2, 96000.0), ("Profesyonel servis (saat)", 12, 2400.0)]),
    ("FT-2026-0452", "Kuzey Ag Teknolojileri", "2026-10-28", [("Konsol sunucusu 16 port", 1, 48700.0), ("USB-C konsol kablosu", 10, 420.0)]),
]


def fatura_pdf(no, firma, tarih, kalemler, yol, toplam_hatasi=0.0):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, s(f"{firma}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, s(f"FATURA No: {no}    Tarih: {tarih}"), new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, s("Alici: DC Operasyon A.S., Istanbul    Vergi No: 1234567890"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    for b, w in (("Aciklama", 100), ("Miktar", 25), ("Birim fiyat", 30), ("Tutar", 35)):
        pdf.cell(w, 8, b, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    ara = 0.0
    for ad, adet, fiyat in kalemler:
        tutar = adet * fiyat
        ara += tutar
        for v, w in ((s(ad), 100), (str(adet), 25), (f"{fiyat:,.2f}", 30), (f"{tutar:,.2f}", 35)):
            pdf.cell(w, 8, v, border=1)
        pdf.ln()
    kdv = round(ara * 0.20, 2)
    pdf.ln(2)
    for etiket, deger in (("Ara toplam", ara), ("KDV %20", kdv), ("GENEL TOPLAM (TL)", ara + kdv + toplam_hatasi)):
        pdf.cell(155, 7, etiket, align="R")
        pdf.cell(35, 7, f"{deger:,.2f}", border=1, align="R")
        pdf.ln()
    pdf.output(str(yol))


def topoloji_png(yol):
    im = Image.new("RGB", (900, 520), "white")
    d = ImageDraw.Draw(im)
    kutular = {
        "SPINE-01": (220, 40), "SPINE-02": (560, 40),
        "LEAF-101": (60, 260), "LEAF-102": (280, 260), "LEAF-103": (500, 260), "LEAF-104": (720, 260),
        "FW-01": (390, 440),
    }
    for a in ("SPINE-01", "SPINE-02"):
        for b in ("LEAF-101", "LEAF-102", "LEAF-103", "LEAF-104"):
            (x1, y1), (x2, y2) = kutular[a], kutular[b]
            d.line((x1 + 60, y1 + 50, x2 + 60, y2), fill="black", width=2)
    d.line((kutular["LEAF-103"][0] + 60, 310, kutular["FW-01"][0] + 60, 440), fill="red", width=3)
    d.line((kutular["LEAF-104"][0] + 60, 310, kutular["FW-01"][0] + 60, 440), fill="red", width=3)
    d.line((kutular["LEAF-101"][0] + 120, 285, kutular["LEAF-102"][0], 285), fill="blue", width=3)
    d.text((190, 290), "vPC peer-link", fill="blue")
    d.text((470, 400), "Eth1/47-48", fill="red")
    for ad, (x, y) in kutular.items():
        d.rectangle((x, y, x + 120, y + 50), outline="black", width=2, fill="#eef3ff")
        d.text((x + 18, y + 18), ad, fill="black")
    d.text((20, 495), "DC1 - kurgusal topoloji (her leaf her spine'a 100G)", fill="gray")
    im.save(yol)


SOZLESME = [
    ("1. Taraflar ve konu", "Bu sozlesme DC Operasyon A.S. (Musteri) ile Kuzey Ag Teknolojileri (Saglayici) arasinda, Musteri'nin DC1 veri merkezindeki ag cihazlarinin bakim ve destek hizmetlerini kapsar. Kapsamdaki cihaz listesi Ek-1'dedir."),
    ("2. Hizmet seviyeleri", "Kritik ariza (uretim trafigi kesik): 30 dakika icinde mudahale, 4 saat icinde gecici cozum. Yuksek ariza (yedeklilik kaybi): 2 saat icinde mudahale, 1 is gunu icinde cozum. Normal talepler: 1 is gunu icinde donus. Hizmet 7/24 verilir."),
    ("3. Yedek parca", "Saglayici, kapsamdaki her cihaz modeli icin Istanbul deposunda en az bir yedek bulundurur. Ariza tespit edilen parca, kritik arizalarda 4 saat, diger durumlarda sonraki is gunu (NBD) icinde sahada teslim edilir. Sokulen parca 15 gun icinde Saglayici'ya iade edilir."),
    ("4. Yazilim guncellemeleri", "Saglayici, ureticinin onerdigi guvenlik guncellemelerini yayinlanmasindan itibaren 30 gun icinde Musteri'ye bildirir. Guncellemeler Musteri'nin bakim penceresinde, Musteri onayi ile uygulanir."),
    ("5. Raporlama", "Saglayici her ayin ilk 5 is gunu icinde onceki aya ait olay, cozum suresi ve SLA uyum raporunu iletir. SLA uyumu %95'in altina duserse o ayin hizmet bedelinden %10 indirim yapilir."),
    ("6. Gizlilik", "Taraflar, hizmet sirasinda edindikleri konfigurasyon, IP adresi ve musteri bilgilerini ucuncu kisilerle paylasmaz. Uzaktan erisim yalnizca Musteri'nin sagladigi VPN ve PAM sistemi uzerinden yapilir."),
    ("7. Sure ve fesih", "Sozlesme 1 Ocak 2027'de baslar ve 12 ay surer. Taraflardan biri sure bitiminden 60 gun once yazili bildirimde bulunmazsa 12 ay uzar. Ust uste iki ay SLA uyumu %90'in altinda kalirsa Musteri sozlesmeyi tazminatsiz feshedebilir."),
    ("8. Ucret", "Yillik hizmet bedeli 1.240.000 TL + KDV'dir ve uc aylik donemler halinde pesin faturalanir. Kapsam disi isler icin saatlik ucret 2.400 TL + KDV'dir."),
]


def sozlesme_pdf(yol):
    pdf = FPDF()
    pdf.set_auto_page_break(True, 20)
    for i, (baslik, metin) in enumerate(SOZLESME):
        if i % 2 == 0:
            pdf.add_page()
            pdf.set_font("Helvetica", "I", 8)
            pdf.cell(0, 5, f"Bakim ve Destek Sozlesmesi - Sayfa {pdf.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, baslik, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, metin)
        pdf.ln(6)
    pdf.output(str(yol))


def main() -> None:
    (KOK / "faturalar").mkdir(exist_ok=True)
    for i, (no, firma, tarih, kalemler) in enumerate(FATURALAR, 1):
        fatura_pdf(no, firma, tarih, kalemler, KOK / "faturalar" / f"fatura-{i}.pdf", toplam_hatasi=1000.0 if i == 4 else 0.0)
    topoloji_png(KOK / "topoloji.png")
    sozlesme_pdf(KOK / "sozlesme.pdf")
    print("Üretildi:", KOK / "faturalar", KOK / "topoloji.png", KOK / "sozlesme.pdf")


if __name__ == "__main__":
    main()
