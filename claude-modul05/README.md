# Claude modül 5 · Envanter araçları ve MCP server

Portaldaki karşılığı: **5. Araç kullanımı ve MCP**, Lab 5.1.

| Dosya | Kavram |
| --- | --- |
| `araclar.py` | `switch_durumu`, `config_farki`, `doviz_kuru` fonksiyonları ve Claude API araç tanımları (kurgusal veri) |
| `dongu.py` | Elle yazılmış tool use döngüsü, `is_error`, paralel sonuçlar (TODO'lar sizde) |
| `runner.py` | Aynı iş Tool Runner ile |
| `envanter_server.py` | MCP server: araçlar + bir resource (TODO'lar sizde) |
| `api_istemci.py` | Server'a stdio ile bağlanıp araçlarını Claude API'ye veren client |

```
 dongu.py / runner.py           araçlar uygulamanın içinde
 api_istemci.py  ── stdio ──▶  envanter_server.py  ◀── stdio ──  Claude Code / Claude Desktop / Inspector
```

Adımlar [HOWTO.md](HOWTO.md)'de.
