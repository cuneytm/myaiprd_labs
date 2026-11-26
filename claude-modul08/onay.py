"""
Claude modül 8 · Onay kapısı: 2.000 TL üstü iade insan onayı olmadan yapılamaz. Bölüm 8.3.

ONAY_MODU ortam değişkeni:
    sor (varsayılan)   terminalde sorar
    otomatik-red       eşik üstü her iadeyi reddeder (degerlendir.py bunu kullanır)
"""
import os

from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny

ESIK_TL = 2000


async def onay_kapisi(arac: str, girdi: dict, baglam) -> PermissionResultAllow | PermissionResultDeny:
    if arac != "mcp__magaza__iade_baslat":
        return PermissionResultAllow(updated_input=girdi)
    tutar = float(girdi.get("tutar", 0))
    if tutar <= ESIK_TL:
        return PermissionResultAllow(updated_input=girdi)
    # TODO: Eşik üstü iade için insana sorun. ONAY_MODU "otomatik-red" ise sormadan reddedin.
    #   if os.getenv("ONAY_MODU") == "otomatik-red": return PermissionResultDeny(message=...)
    #   cevap = input(f"[onay] {girdi['siparis_no']} için {tutar:.2f} TL iade onaylansın mı? (e/h) ")
    #   ...
    _ = os
    return PermissionResultAllow(updated_input=girdi)       # şimdilik kapı açık: TODO'yu tamamlayın
