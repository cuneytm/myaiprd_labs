"""Aday şeması. json_dogrula aracı ajanın ürettiği JSON'u bu şemaya göre doğrular."""
from pydantic import BaseModel, Field


class Pozisyon(BaseModel):
    unvan: str
    sirket: str
    baslangic_yili: int
    bitis_yili: int | None = Field(description="Hâlâ devam ediyorsa null")


class Aday(BaseModel):
    ad: str
    eposta: str | None
    deneyim_yili: int | None = Field(description="Özgeçmişte açıkça yazmıyorsa null; tahmin etme")
    sertifikalar: list[str]
    teknolojiler: list[str]
    son_pozisyonlar: list[Pozisyon] = Field(max_length=3)
    eksik: list[str] = Field(description="Bulunamayan zorunlu alanların adları")
