# Claude modül 3 · Değişiklik talebi çıkarıcı

Portaldaki karşılığı: **3. Prompt tasarımı ve performans**, Lab 3.1.

| Dosya | Kavram |
| --- | --- |
| `sema.py` | Pydantic şeması (`DegisiklikTalebi`) |
| `cikarici.py` | `messages.parse`, iş kuralı doğrulaması, yeniden deneme (TODO'lar sizde) |
| `onbellek_olc.py` | Aynı runbook ile 5 istek; `cache_read_input_tokens` ölçümü |
| `toplu.py` | 50 talebi Batch API ile gönderme, `custom_id` ile eşleme |
| `veri/talepler.jsonl` | 50 kurgusal değişiklik talebi, 5'inde bilerek hatalı VLAN |
| `veri/runbook.md` | Kurgusal DC1 değişiklik runbook'u (system prompt'ta, önbellekte) |

Adımlar [HOWTO.md](HOWTO.md)'de.
