# Modül 2 · Nasıl çalışır, ne yapacaksınız

Önce depo kökündeki [README.md](../README.md)'deki kurulumu yapın. Modül 1'i tamamladıysanız sanal ortam ve `.env` hazırdır. Sonra:

```bash
cd modul02-mcp
```

`[server] ...` ile başlayan satırlar MCP server'ın loglarıdır (stderr). Server'ın neyi, ne zaman çalıştırdığını buradan görürsünüz.

---

## Adım 1 · Server'ı tanıyın

`server.py` ile Modül 1'deki `tools.py`'yi yan yana açın. Dört fonksiyonun gövdesi aynıdır. Farklar:

- Her fonksiyonun üstünde `@mcp.tool` var. Ayrıca açıklama ve JSON Schema yazmadık: SDK bunları **docstring**'den ve **parametre tiplerinden** üretir.
- `@mcp.resource` ve `@mcp.prompt`: MCP'nin diğer iki primitifi.
- `mcp.run()`: transport belirtilmediği için **stdio**.

Server'ı `python server.py` ile doğrudan çalıştırırsanız hiçbir şey olmuyormuş gibi bekler: stdin'den JSON-RPC mesajı bekliyordur. `Ctrl+C` ile çıkın. Server'ı her zaman bir host başlatır.

## Adım 2 · Modelsiz client: host ile server ne konuşur?

```bash
python client_test.py
```

**Gözlemleyin:**
1. Client server'ı alt süreç olarak başlatır ve bağlanır.
2. **Keşif:** `tools/list` her tool'un adını, açıklamasını ve parametrelerini döndürür. `resources/list` ve `prompts/list` diğer iki primitifi listeler.
3. **Çağrı:** `tools/call` ile `list_files` ve `search_files` çalışır; `resources/read` ve `prompts/get` de birer kez çağrılır.

Bu adımda model yok: neyin çağrılacağına kod karar verdi. Bir sonraki adımda model karar verecek.

### İsteğe bağlı: MCP Inspector

Node.js kuruluysa server'ı tarayıcıdan deneyebilirsiniz:

```bash
npx @modelcontextprotocol/inspector python server.py
```

Açılan sayfada **Connect**'e basın; Tools, Resources ve Prompts sekmelerinden her birini elle çağırın.

## Adım 3 · Agent + MCP

```bash
python agent_mcp.py
```

Başlangıçta `MCP server'dan 4 tool alındı` satırını görürsünüz. `agent_mcp.py`'de hiçbir tool tanımı yoktur; hepsi server'dan gelir.

Modül 1'de verdiğiniz görevleri burada da verin:

```
Siz> Klasörde hangi dosyalar var?
Siz> Yapılacaklar listesinde bitmemiş işler hangileri?
Siz> Toplantı notlarını özetle ve TOPLANTI-OZETI.md olarak kaydet.
```

**Gözlemleyin:**
- `[adım N · MCP tools/call]` satırı agent'ın server'a gönderdiği çağrıdır; hemen ardından gelen `[server]` satırı server'ın onu çalıştırdığı andır. İki ayrı süreç konuşuyor.
- Sonuçlar Modül 1 ile aynı mı? Olmalı: tool'lar aynı, yalnız nerede çalıştıkları değişti.

`agent_mcp.py`'deki `run_task()` ile Modül 1'deki `run_task()`'ı yan yana açın. Değişen tek önemli satır, tool'un çalıştırıldığı satırdır: `ALL_TOOLS[name]["fn"](...)` yerine `await client.call_tool(...)`.

## Adım 4 (isteğe bağlı) · Aynı server'ı Claude Desktop'a bağlamak

MCP'nin değeri, bir kez yazılan server'ın farklı host'larda kullanılabilmesidir. Claude Desktop kuruluysa:

1. Sanal ortamdaki Python'un ve server'ın tam yolunu öğrenin (depo kökünde):

   ```bash
   echo "$(pwd)/.venv/bin/python"
   echo "$(pwd)/modul02-mcp/server.py"
   ```

2. Claude Desktop'ta **Settings → Developer → Edit Config** ile `claude_desktop_config.json` dosyasını açın ve ekleyin (yolları kendi çıktınızla değiştirin):

   ```json
   {
     "mcpServers": {
       "calisma-klasoru": {
         "command": "/Users/kullaniciadi/myaiprd_labs/.venv/bin/python",
         "args": ["/Users/kullaniciadi/myaiprd_labs/modul02-mcp/server.py"]
       }
     }
   }
   ```

3. Claude Desktop'u kapatıp açın. Sohbette "Çalışma klasörümde hangi dosyalar var?" diye sorun.

Server'da tek satır değişmedi; değişen yalnız host'tur.

---

## Alıştırmalar

1. **Yeni tool, sıfır agent değişikliği:** `server.py`'ye `file_info(path)` tool'u ekleyin (dosya boyutu ve son değiştirilme tarihi: `f.stat().st_size`, `f.stat().st_mtime`). Fonksiyonun üstüne `@mcp.tool` yazmanız ve iyi bir docstring vermeniz yeterli. `client_test.py`'yi çalıştırın: yeni tool listede mi? Sonra agent'a "en son hangi dosya değişti?" diye sorun. `agent_mcp.py`'de bir değişiklik yaptınız mı?
2. **Docstring'in gücü:** `search_files`'ın docstring'ini "Arama yapar." olarak kısaltın ve `client_test.py`'de açıklamanın nasıl değiştiğine bakın. Agent'a dosya adını vermeden bir şey sorun; model hâlâ bu tool'u seçiyor mu?
3. **Başka bir klasör:** `.env`'de `WORK_DIR`'ı başka bir klasöre çevirin. Server'ın kodunda bir değişiklik gerekti mi?
4. **Resource ve prompt'u kim kullanır?** Agent, `klasor://dosyalar` resource'unu ve `ozetle` prompt'unu kendiliğinden kullandı mı? Neden? (İpucu: `agent_mcp.py` modele yalnız neyi veriyor?) Claude Desktop'ta bu ikisini nerede görürsünüz?
5. **İki server:** Modül 1'deki skill'leri sunan ikinci küçük bir MCP server düşünün (`list_skills`, `load_skill`). Agent iki server'a nasıl bağlanırdı? (Kod yazmak zorunlu değil; tasarımı tartışın.)

## Tartışma soruları

- Server stdio ile, sizin bilgisayarınızda ve sizin kullanıcı yetkilerinizle çalışıyor. Başkasının yazdığı bir MCP server'ı kurmadan önce neye bakarsınız?
- Aynı server'ı ekipteki herkes kullanacak olsaydı stdio yeterli olur muydu? Ne değişirdi? (Streamable HTTP, kimlik doğrulama)
- Bir tool'u agent'ın kodunda mı, MCP server'da mı tanımlamak daha doğru? Hangi durumda hangisi?

## Sorun giderme

| Belirti | Neden ve çözüm |
| --- | --- |
| `No module named 'mcp'` | Sanal ortam aktif değil (`source ../.venv/bin/activate`) ya da `pip install -r requirements.txt` yapılmadı. `pip` mcp için hata verdiyse Python sürümünüz 3.10'dan eski: `python3 --version` (macOS'un yerleşik `python3`'ü 3.9'dur; `brew install python@3.12` ile kurup sanal ortamı onunla yeniden oluşturun) |
| `No module named 'mcp.server.fastmcp'` | İnternetteki eski (1.x) örneklerden kod kopyalandı. Bu laboratuvar MCP Python SDK 2.x kullanır: `from mcp.server.mcpserver import MCPServer` |
| Client bağlanırken takılıyor ya da JSON hatası veriyor | `server.py` içinde `print()` kullanıldıysa stdout bozulur. Log için `log.info()` kullanın |
| Server yanlış klasörü sunuyor | `client_test.py` çıktısındaki `[server] çalışma klasörü:` satırına bakın; `.env`'deki `WORK_DIR` tam yol olmalı |
| Model tool çağırmıyor | Modelin tool calling desteğini kontrol edin (Modül 1 HOWTO, Sorun giderme) |
| Claude Desktop server'ı görmüyor | Config'teki yollar tam (mutlak) olmalı ve sanal ortamdaki Python'u göstermeli; Claude Desktop'u tamamen kapatıp açın |
