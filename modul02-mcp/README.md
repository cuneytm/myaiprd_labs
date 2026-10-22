# Modül 2 · MCP: dosya tool'larını bir MCP server'da yayınlamak

Modül 1'de agent, dosya tool'larını kendi kodunda (`tools.py`) tanımlıyordu. Bu tool'ları yalnız o agent kullanabiliyordu. Bu modülde **aynı dört fonksiyonu** bir **MCP server**'a taşıyoruz. Artık MCP destekleyen her uygulama (bu laboratuvardaki agent, MCP Inspector, Claude Desktop...) aynı tool'ları kullanabilir.

| Adım | Dosya | Ne öğrenirsiniz |
| --- | --- | --- |
| 1 | `server.py` | MCP server neyi sunar: tools, resources, prompts |
| 2 | `client_test.py` | Host ile server ne konuşur: bağlan, keşfet (`tools/list`), çağır (`tools/call`). **Model yok** |
| 3 | `agent_mcp.py` | Agent tool'ları MCP server'dan alır; hangi tool'un çağrılacağını model önerir |
| 4 | (isteğe bağlı) Claude Desktop | Aynı server'ı hiç kod yazmadan başka bir host'a bağlamak |

```
 agent_mcp.py (HOST)                    server.py (MCP SERVER)
 ┌──────────────────────────┐   stdio   ┌──────────────────────┐
 │ model + loop             │ ────────▶ │ list_files           │ ──▶  WORK_DIR
 │ MCP client               │ ◀──────── │ read_file  ...       │      (sizin klasörünüz)
 └──────────────────────────┘ JSON-RPC  └──────────────────────┘
```

## Modül 1 ile ne değişti?

| | Modül 1 | Modül 2 |
| --- | --- | --- |
| Tool'lar nerede tanımlı | Agent'ın kodunda (`tools.py`) | MCP server'da (`server.py`) |
| Agent tool'ları nasıl öğreniyor | Kendi sözlüğünden | Başlangıçta server'a sorarak (`tools/list`) |
| Tool'u kim çalıştırıyor | Agent, fonksiyonu doğrudan çağırır | Agent server'a `tools/call` gönderir, server çalıştırır |
| Tool'u kimler kullanabilir | Yalnız bu agent | MCP destekleyen her host |
| Agent döngüsü | `run_task()` | Aynı `run_task()`; yalnız tool çağırma satırı farklı |

## Kavram → dosya haritası

| Kavram | Nerede | Ne görürsünüz |
| --- | --- | --- |
| **Host, client, server** | `agent_mcp.py` (host + client), `server.py` (server) | Host, server'ı alt süreç olarak başlatır; her server için bir client |
| **Transport: stdio** | `StdioServerParameters`, `mcp.run()` | Mesajlar stdin/stdout'tan geçer, ağ yok. Server logu stderr'e yazar, çünkü stdout protokole aittir |
| **Tools** (model kontrollü) | `@mcp.tool` | Fonksiyonun docstring'i açıklama, parametreleri JSON Schema olur |
| **Resources** (uygulama kontrollü) | `@mcp.resource("klasor://dosyalar")` | Okunabilir veri; context'e ne zaman ekleneceğine uygulama karar verir |
| **Prompts** (kullanıcı kontrollü) | `@mcp.prompt` → `ozetle` | Kullanıcının menüden seçtiği hazır şablon |
| **Keşif** | `client_test.py`, `agent_mcp.py` | `tools/list` ile ad, açıklama ve şema gelir |
| **Şema çevirisi** | `agent_mcp.py` → `to_openai_tools()` | MCP tool tanımı ile modelin tool tanımı aynı içeriktir: ad, açıklama, JSON Schema |

## Dosyalar

```
modul02-mcp/
├── server.py         MCP server (stdio): 4 tool, 1 resource, 1 prompt
├── client_test.py    modelsiz MCP client: bağlan, keşfet, çağır
└── agent_mcp.py      agent + MCP entegrasyonu
```

Server, `.env`'deki `WORK_DIR` klasörünü sunar (boşsa depodaki `ornek-klasor`); Modül 1 ile aynı klasör.

Adım adım çalıştırma ve alıştırmalar: **[HOWTO.md](HOWTO.md)**
