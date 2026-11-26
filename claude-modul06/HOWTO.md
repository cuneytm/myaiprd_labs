# Claude modül 6 · Ne yapacaksınız

```bash
cd claude-modul06
python veri/ornek_uret.py
```

## Adım 1 · TODO'lar

`ajan.py`'de:

1. **TODO 1:** System prompt'a bitiş koşulunu yazın.
2. **TODO 2:** `allowed_tools`'a izinsiz çalışacak araçları ekleyin (`mcp__ozgecmis__dosyalari_listele`, `mcp__ozgecmis__pdf_oku`, `mcp__ozgecmis__json_dogrula`). `kaydet`'i eklemeyin.
3. **TODO 3:** `max_turns` verin.

## Adım 2 · Üç dosyada deneyin

```bash
python ajan.py --ilk 3
```

Her `kaydet` çağrısında terminal onay ister (`onay.py`). Araç çağrıları `→` ile yazdırılır.

## Adım 3 · Tüm klasör

```bash
python ajan.py
```

`adaylar/` klasöründeki JSON'ları ve sondaki özet tabloyu kontrol edin.

**Gözlemleyin:**

- 05 ve 14 numaralı özgeçmişlerde deneyim yılı yazmıyor. Ajan ne yaptı: sordu mu, uydurdu mu, `eksik`'e mi yazdı?
- `json_dogrula` hata verdiğinde ajan kaç denemede düzeltti?
- `max_turns`'ü 5'e düşürünce ne oldu? Ajan işin yarısında nasıl durdu?
- Bir kaydı reddettiğinizde ajan nasıl devam etti?

## Alıştırma

Bir `PreToolUse` hook'u ekleyin: `kaydet` çağrısında `deneyim_yili` 40'tan büyükse çağrıyı engellesin ve ajana "değeri tekrar kontrol et" mesajı dönsün.

İpucu:

```python
from claude_agent_sdk import HookMatcher

async def yil_kontrol(girdi, tool_use_id, baglam):
    ...  # girdi["tool_input"]["json"] içinden deneyim_yili'ni okuyun
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                   "permissionDecision": "deny",
                                   "permissionDecisionReason": "deneyim_yili 40'tan büyük; değeri tekrar kontrol et"}}

# ClaudeAgentOptions(..., hooks={"PreToolUse": [HookMatcher(matcher="mcp__ozgecmis__kaydet", hooks=[yil_kontrol])]})
```
