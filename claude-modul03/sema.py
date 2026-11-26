"""Değişiklik talebi şeması (Bölüm 3.4). Structured outputs bu şemaya uygun JSON garanti eder."""
from typing import Literal

from pydantic import BaseModel, Field


class DegisiklikTalebi(BaseModel):
    cihaz: str = Field(description="Etkilenen cihaz(lar), talepte yazdığı gibi. Birden fazlaysa virgülle.")
    islem: Literal["ekle", "sil", "degistir"]
    vlan_id: int | None = Field(description="Talepteki VLAN numarası, olduğu gibi. Yoksa null.")
    bakim_penceresi_gerekli: bool
    risk: Literal["dusuk", "orta", "yuksek"]
    ozet: str = Field(description="Tek cümlelik özet; belirsizlik veya kural ihlali varsa belirt.")
