"""
Claude modül 6 · 20 kurgusal özgeçmiş PDF'i üretir (veri/ozgecmisler/).
Biçimler bilerek farklıdır: kronolojik, beceri odaklı, kısa paragraf; bazılarında
deneyim yılı veya sertifika bilgisi yoktur.

    python veri/ornek_uret.py
"""
import random
from pathlib import Path

from fpdf import FPDF

KOK = Path(__file__).parent
SADE = str.maketrans("şŞğĞıİçÇöÖüÜ", "sSgGiIcCoOuU")
random.seed(11)

ADLAR = ["Ayse Demir", "Mehmet Kaya", "Zeynep Arslan", "Can Yildiz", "Elif Sahin", "Burak Celik", "Deniz Aydin",
         "Ece Koc", "Emre Kurt", "Selin Ozturk", "Kaan Aksoy", "Merve Polat", "Onur Erdem", "Pinar Tas",
         "Serkan Gunes", "Tugba Yalcin", "Umut Sen", "Yasemin Acar", "Baris Kara", "Gizem Cetin"]
SERT = ["CCNP Enterprise", "CCNA", "CCIE Data Center", "JNCIA-Junos", "AWS Advanced Networking", "CKA", "Fortinet NSE 4"]
TEKNO = ["VXLAN EVPN", "BGP", "OSPF", "NX-OS", "Ansible", "Python", "NetBox", "Terraform", "Palo Alto", "F5",
         "Kubernetes", "SD-WAN", "Wireshark", "Grafana", "Junos"]
SIRKETLER = ["Atlas Lojistik", "Deniz Finans", "Kuzey Enerji", "Mavi Saglik", "Orion Yazilim", "Pera Perakende",
             "Tuna Telekom", "Selin Medya"]
UNVAN = ["Network Engineer", "Senior Network Engineer", "NOC Specialist", "Network Automation Engineer",
         "Data Center Engineer", "Infrastructure Lead"]


def kisi(i):
    yil = random.randint(2, 18)
    poz = []
    bitis = 2026
    for _ in range(random.randint(2, 4)):
        bas = bitis - random.randint(1, 5)
        poz.append((random.choice(UNVAN), random.choice(SIRKETLER), bas, bitis))
        bitis = bas
    return {
        "ad": ADLAR[i], "yil": yil,
        "sert": random.sample(SERT, random.randint(0, 3)),
        "tek": random.sample(TEKNO, random.randint(4, 8)),
        "poz": poz,
        "eposta": ADLAR[i].lower().replace(" ", ".") + "@ornek.test",
        "bicim": i % 3, "yil_yok": i in (4, 13), "sert_yok": i in (7,),
    }


def pdf_yaz(k, yol):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, k["ad"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"{k['eposta']}  |  Istanbul", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    def yaz(t):
        pdf.multi_cell(0, 5, t, new_x="LMARGIN", new_y="NEXT")

    def baslik(t):
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, t, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)

    ozet = "" if k["yil_yok"] else f"{k['yil']} yillik deneyime sahip "
    if k["bicim"] == 0:            # kronolojik
        baslik("Ozet")
        yaz(f"{ozet}ag muhendisi. Veri merkezi ve kampus aglarinda calistim.")
        baslik("Deneyim")
        for u, s, b, e in k["poz"]:
            yaz(f"{b} - {e if e < 2026 else 'halen'}: {u}, {s}")
        baslik("Teknolojiler")
        yaz(", ".join(k["tek"]))
        if not k["sert_yok"]:
            baslik("Sertifikalar")
            yaz(", ".join(k["sert"]) or "-")
    elif k["bicim"] == 1:          # beceri odaklı
        baslik("Yetkinlikler")
        for t in k["tek"]:
            yaz(f"- {t}")
        if not k["sert_yok"] and k["sert"]:
            baslik("Belgeler")
            for c in k["sert"]:
                yaz(f"* {c}")
        baslik("Is gecmisi")
        for u, s, b, e in k["poz"]:
            yaz(f"{s} ({b}-{e if e < 2026 else 'gunumuz'}) - {u}")
        if not k["yil_yok"]:
            yaz(f"Toplam deneyim: {k['yil']} yil")
    else:                          # paragraf
        baslik("Hakkimda")
        son = k["poz"][0]
        metin = (f"{ozet}bir muhendisim. Su anda {son[1]} sirketinde {son[0]} olarak calisiyorum. "
                 f"Daha once {', '.join(p[1] for p in k['poz'][1:])} sirketlerinde gorev aldim. "
                 f"Gunluk isimde {', '.join(k['tek'][:-1])} ve {k['tek'][-1]} kullaniyorum.")
        if k["sert"] and not k["sert_yok"]:
            metin += f" {' ve '.join(k['sert'])} sertifikalarim var."
        yaz(metin)
    pdf.output(str(yol))


def main():
    hedef = KOK / "ozgecmisler"
    hedef.mkdir(exist_ok=True)
    for i in range(20):
        k = kisi(i)
        pdf_yaz(k, hedef / f"{i + 1:02d}-{k['ad'].split()[0].lower()}.pdf")
    print("20 özgeçmiş üretildi:", hedef)


if __name__ == "__main__":
    main()
