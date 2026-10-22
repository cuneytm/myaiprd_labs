# Modül 1 · AI Agent

Bu laboratuvarda bir agent'ın parçalarını kodda göreceksiniz:

```
agent = model + harness
harness = instructions + tools + skills + memory + loop
```

**Model** yalnız bir sonraki adımı önerir: "şu tool'u şu argümanla çağır" ya da "cevap şu". Tool'u çalıştıran, hatırlayan ve döngüyü yöneten **harness**'tır, yani `agent.py`.

Agent, `.env`'de verdiğiniz klasör (`WORK_DIR`) üzerinde çalışır. Ona "toplantı notlarını özetle", "yapılacaklar listesinde bitmemiş işler hangileri", "klasör için bir rapor yaz ve kaydet" gibi işler verirsiniz; agent hangi dosyayı okuyacağına ve ne yapacağına kendisi karar verir.

## Kavram → dosya haritası

| Kavram | Nerede | Ne görürsünüz |
| --- | --- | --- |
| **Model** | `.env` (adres, ad, anahtar) | Modeli değiştirmek için kodu değil `.env`'i değiştirirsiniz |
| **Instructions** | `instructions.md` | Rol ve kurallar; her model çağrısında context'in başına konur |
| **Task** | `agent.py` → sohbet, `--task`, `--tasks` | İşin kendisi; her seferinde değişir. Aynı agent'a iş üç yoldan gelebilir |
| **Tools** | `tools.py` | Dört dosya tool'u: `list_files`, `read_file`, `search_files`, `write_file`. Her biri fonksiyon + açıklama + JSON Schema |
| **Tool calling** | `agent.py` → `run_task()` | Model `tool_calls` döndürür; harness fonksiyonu çalıştırır; sonuç `role: "tool"` mesajıyla context'e eklenir |
| **Skills** | `skills/*/SKILL.md` | Context'te yalnız katalog (ad + açıklama) durur; model gerekince `load_skill` ile tam talimatı ister |
| **Memory** | `agent.py` → MEMORY bölümü, `memory/` klasörü | short-term: `messages` listesi (son görevin kopyası `memory/son-gorev-context.json`) · session: `memory/session.json` (yalnız sohbette, `--resume`) · long-term: `memory/facts.md` (yalnız model `remember` çağırınca) · procedural: skill'ler |
| **Loop (iç döngü)** | `agent.py` → `run_task()` | Modeli çağır → tool'u çalıştır → sonucu ekle → tekrar; model tool önermeden cevap verince durur |
| **Dış döngü** | `agent.py` → `run_queue()`, `tasks.txt` | Kuyruktaki her görev ayrı ve temiz bir context ile çalışır |
| **Workflow ile farkı** | `workflow.py` | Benzer bir işte adımları kod seçer, model yalnız özetler |

## Dosyalar

```
modul01-ai-agent/
├── agent.py          harness: model çağrısı, loop, memory, skill yükleme
├── tools.py          dosya tool'ları (Modül 2'de MCP server'a taşınacak)
├── workflow.py       karşılaştırma: sabit adımlı workflow
├── instructions.md   system instructions
├── skills/
│   ├── klasor-raporu/SKILL.md     klasör raporu prosedürü
│   └── toplanti-ozeti/SKILL.md    toplantı notlarından karar ve aksiyon çıkarma
├── tasks.txt         dış döngü için görev kuyruğu
└── memory/           (çalışınca oluşur) son-gorev-context.json, session.json, facts.md, kuyruk sonuçları
```

`ornek-klasor` ile çalışıyorsanız skill'ler oradaki dosyalara (toplantı notları, yapılacaklar listesi, proje planı) uygundur. Kendi klasörünüzle de çalışırlar.

Adım adım çalıştırma ve alıştırmalar: **[HOWTO.md](HOWTO.md)**
