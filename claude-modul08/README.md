# Claude modül 8 · Alt ajanlı sipariş ve destek asistanı

Portaldaki karşılığı: **8. Çok adımlı ajanlar ve güvenilirlik**, Lab 8.1.

| Dosya | Kavram |
| --- | --- |
| `magaza_server.py` | Kurgusal mağaza MCP server'ı: `siparis_getir`, `urun_ara`, `iade_baslat` |
| `veri/` | 50 sipariş, 120 ürün, kurgusal ve maskeli müşteriler |
| `asistan.py` | Orkestratör ve alt ajanlar (TODO'lar sizde) |
| `onay.py` | 2.000 TL üstü iade için terminal onayı (TODO sizde) |
| `senaryolar/` | 10 test mesajı (07 ve 09 injection içerir) ve beklenen davranışlar |
| `degerlendir.py` | Senaryoları çalıştırır, server logundan davranışı kontrol eder |

```
 müşteri ─▶ orkestratör (Opus) ──▶ siparis-uzmani (Sonnet) ──┐
                              └──▶ urun-uzmani (Haiku) ──────┤── stdio ──▶ magaza_server.py
                                    onay kapısı (iade > 2.000 TL)
```

**Ek gereksinim:** Claude Code kurulu olmalı (Agent SDK onu motor olarak kullanır).
