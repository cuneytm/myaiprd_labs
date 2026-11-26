"""
Claude modül 5 · Araç fonksiyonları ve Claude API için araç tanımları (kurgusal veri).

Bu fonksiyonlar sıradan Python'dur; Claude kodu görmez, yalnız TOOLS içindeki
name / description / input_schema'yı görür. Bölüm 5.1 ve 5.3.
"""
import difflib

ENVANTER = {
    "LEAF-101": {"fabric": "DC1-FABRIC", "rol": "leaf", "sync": "In-Sync", "nxos": "10.4(3)"},
    "LEAF-102": {"fabric": "DC1-FABRIC", "rol": "leaf", "sync": "In-Sync", "nxos": "10.4(3)"},
    "LEAF-103": {"fabric": "DC1-FABRIC", "rol": "leaf", "sync": "Out-of-Sync", "nxos": "10.4(3)"},
    "LEAF-104": {"fabric": "DC1-FABRIC", "rol": "leaf", "sync": "Out-of-Sync", "nxos": "10.4(3)"},
    "SPINE-01": {"fabric": "DC1-FABRIC", "rol": "spine", "sync": "In-Sync", "nxos": "10.4(3)"},
    "SPINE-02": {"fabric": "DC1-FABRIC", "rol": "spine", "sync": "In-Sync", "nxos": "10.4(3)"},
    "BORDER-01": {"fabric": "DC1-FABRIC", "rol": "border", "sync": "In-Sync", "nxos": "10.3(5)"},
    "LEAF-201": {"fabric": "DC2-FABRIC", "rol": "leaf", "sync": "In-Sync", "nxos": "10.2(7)"},
    "LEAF-202": {"fabric": "DC2-FABRIC", "rol": "leaf", "sync": "In-Sync", "nxos": "10.2(7)"},
    "SPINE-21": {"fabric": "DC2-FABRIC", "rol": "spine", "sync": "In-Sync", "nxos": "10.2(7)"},
}

# Beklenen (NDFC'deki) ve çalışan config arasındaki farklar: out-of-sync cihazlar için
_ORTAK = """interface Ethernet1/12
  description SRV-DB-07
  switchport access vlan 2150
  mtu 9216
ntp server 10.10.0.1 use-vrf management
logging server 10.10.0.5 6 use-vrf management
"""
CONFIG = {
    "LEAF-103": (_ORTAK, _ORTAK.replace("mtu 9216", "mtu 1500")),
    "LEAF-104": (_ORTAK, _ORTAK.replace("ntp server 10.10.0.1 use-vrf management\n", "")
                 + "interface Ethernet1/40\n  shutdown\n"),
}

LISANS_USD = {"leaf": 1450.0, "spine": 2900.0, "border": 3600.0}   # yıllık, cihaz başına
_KUR = {"USD": 34.85, "EUR": 37.60}                                # kurgusal, sabit


def switch_durumu(fabric: str, rol: str = "all") -> str:
    satirlar = [f"{ad}: {d['rol']}, {d['sync']}, NX-OS {d['nxos']}"
                for ad, d in ENVANTER.items()
                if d["fabric"] == fabric and rol in ("all", d["rol"])]
    if not satirlar:
        # Bilerek kötü hata mesajı: Alıştırma 2'de iyileştireceksiniz.
        raise ValueError("bulunamadı")
    return "\n".join(satirlar)


def config_farki(cihaz: str) -> str:
    if cihaz not in ENVANTER:
        raise ValueError(f"{cihaz} envanterde yok. Önce switch_durumu ile cihaz adlarını öğrenin.")
    if cihaz not in CONFIG:
        return f"{cihaz} In-Sync: beklenen ve çalışan config aynı."
    beklenen, calisan = CONFIG[cihaz]
    fark = difflib.unified_diff(beklenen.splitlines(), calisan.splitlines(), "beklenen (NDFC)", "calisan", lineterm="")
    return "\n".join(fark)


def doviz_kuru(para_birimi: str) -> str:
    kur = _KUR.get(para_birimi.upper())
    if kur is None:
        raise ValueError(f"{para_birimi} desteklenmiyor. Desteklenenler: {', '.join(_KUR)}")
    return f"1 {para_birimi.upper()} = {kur} TRY (kurgusal sabit kur)"


ARACLAR = {"switch_durumu": switch_durumu, "config_farki": config_farki, "doviz_kuru": doviz_kuru}

TOOLS = [
    {
        "name": "switch_durumu",
        "description": ("Bir fabric'teki switch'leri ve config senkron durumlarını listeler. Salt okunurdur. "
                        "'Out-of-sync var mı', 'hangi leaf'ler sorunlu' gibi sorularda kullan. "
                        "Config farkını görmek için kullanma; onun için config_farki var."),
        "input_schema": {
            "type": "object",
            "properties": {
                "fabric": {"type": "string", "description": "Fabric adı, birebir. Örnek: DC1-FABRIC"},
                "rol": {"type": "string", "enum": ["all", "spine", "leaf", "border"]},
            },
            "required": ["fabric"],
            "additionalProperties": False,
        },
    },
    {
        "name": "config_farki",
        "description": ("Bir cihazın NDFC'deki beklenen config'i ile çalışan config'i arasındaki farkı unified diff olarak döner. "
                        "Out-of-sync bir cihazda neyin değiştiğini görmek için kullan. Tek cihaz alır; birden fazla cihaz "
                        "için paralel çağır."),
        "input_schema": {
            "type": "object",
            "properties": {"cihaz": {"type": "string", "description": "Cihaz adı, birebir. Örnek: LEAF-103"}},
            "required": ["cihaz"],
            "additionalProperties": False,
        },
    },
    {
        "name": "doviz_kuru",
        "description": "Döviz kurunu TRY cinsinden döner. Lisans maliyetini TL'ye çevirmek için kullan.",
        "input_schema": {
            "type": "object",
            "properties": {"para_birimi": {"type": "string", "description": "USD veya EUR"}},
            "required": ["para_birimi"],
            "additionalProperties": False,
        },
    },
]
