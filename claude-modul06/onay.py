"""
Claude modül 6 · kaydet aracı çalışmadan önce terminalde onay (can_use_tool). Bölüm 6.4.
"""
import json

from claude_agent_sdk import PermissionResultAllow, PermissionResultDeny


async def onay_iste(arac: str, girdi: dict, baglam) -> PermissionResultAllow | PermissionResultDeny:
    if arac != "mcp__ozgecmis__kaydet":
        return PermissionResultAllow(updated_input=girdi)
    try:
        ozet = json.loads(girdi.get("json", "{}"))
        satir = f"{ozet.get('ad')} · {ozet.get('deneyim_yili')} yıl · eksik: {ozet.get('eksik')}"
    except json.JSONDecodeError:
        satir = girdi.get("json", "")[:120]
    cevap = input(f"\n[onay] {girdi.get('dosya_adi')} kaydedilsin mi? {satir}  (e/h) ").strip().lower()
    if cevap == "e":
        return PermissionResultAllow(updated_input=girdi)
    return PermissionResultDeny(message="Kullanıcı kaydı reddetti. Bu dosyayı atla ve özet tabloda 'reddedildi' yaz.")
