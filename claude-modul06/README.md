# Claude modül 6 · JSON tabanlı özgeçmiş ayrıştırıcı ajan

Portaldaki karşılığı: **6. Ajan geliştirme**, Lab 6.1.

| Dosya | Kavram |
| --- | --- |
| `veri/ornek_uret.py` | Kurgusal, farklı biçimlerde 20 özgeçmiş PDF'i üretir |
| `sema.py` | `Aday` şeması: ad, deneyim yılı, sertifikalar, teknolojiler, son 3 pozisyon, eksikler |
| `araclar.py` | `dosyalari_listele`, `pdf_oku`, `json_dogrula`, `kaydet` (Agent SDK `@tool`) |
| `ajan.py` | Agent SDK ile ajan: araçlar, `max_turns`, durma kuralı (TODO'lar sizde) |
| `onay.py` | `can_use_tool` ile `kaydet` öncesi terminalde onay |

**Ek gereksinim:** Agent SDK, Claude Code'u motor olarak kullanır. `claude --version` çalışmıyorsa Claude Code'u kurun (bkz. portal Bölüm 7.1).

Adımlar [HOWTO.md](HOWTO.md)'de.
