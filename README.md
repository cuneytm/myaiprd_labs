# AI Agent ve MCP laboratuvarları

AI agent'ların ve Model Context Protocol'ün (MCP) temellerini uygulamalı olarak gösteren iki laboratuvar. Kod kısadır ve framework kullanılmaz: agent döngüsünü ve MCP'yi doğrudan görürsünüz. Her dosyanın başında hangi kavramı gösterdiği yazar.

Her iki laboratuvarda da agent, **sizin seçtiğiniz bir klasör** üzerinde sizin verdiğiniz işleri yapar: dosyaları listeler, okur, arar, özetler ve isterseniz yeni dosya yazar.

| Modül | Klasör | Ne yapacaksınız |
| --- | --- | --- |
| 1 · AI Agent | [`modul01-ai-agent`](modul01-ai-agent/) | Instructions, tools, skills, memory ve loop'tan oluşan basit bir agent'ı çalıştırıp inceleyeceksiniz. Dosya işlemleri agent'ın kendi kodundaki tool'larla yapılır |
| 2 · MCP | [`modul02-mcp`](modul02-mcp/) | Aynı dosya işlemlerini bir MCP server'da tool olarak yayınlayacak, önce modelsiz bir client'la, sonra agent'la kullanacaksınız |

Her modülde iki dosya vardır: **README.md** ne öğreneceğinizi ve hangi kavramın hangi dosyada olduğunu anlatır; **HOWTO.md** adım adım ne yapacağınızı ve alıştırmaları verir.

## Gerekenler

- **Python 3.10 veya üstü** (`python3 --version`). macOS'la gelen `python3` 3.9 olabilir; bu durumda `brew install python@3.12` ile yeni bir sürüm kurun ve sanal ortamı `python3.12 -m venv .venv` ile oluşturun. MCP kütüphanesi 3.9'a kurulmaz.
- **Tool calling destekleyen bir model** ve onun OpenAI uyumlu adresi. Örnekler:
  - **Yerel, Ollama:** [ollama.com](https://ollama.com) adresinden kurun, tool destekleyen bir model indirin: `ollama pull qwen3:8b` (16 GB RAM'li bir Mac için uygundur; daha az bellekte `qwen3:4b`). Adres: `http://localhost:11434/v1`
  - **Yerel, LM Studio:** bir model yükleyip local server'ı başlatın. Adres: `http://localhost:1234/v1`
  - **Bulut veya kurum içi:** OpenAI ya da OpenAI uyumlu bir gateway; adres ve API anahtarı gerekir
- **Bir çalışma klasörü.** Agent bu klasörde dosya oluşturabilir ve dosyaların üzerine yazabilir; önemli dosyalarınızın olduğu bir klasör yerine bir kopya ya da test klasörü verin. Klasör vermezseniz depodaki [`ornek-klasor`](ornek-klasor/) kullanılır.
- İsteğe bağlı: Node.js (Modül 2'de MCP Inspector için), Claude Desktop (Modül 2'de server'ı başka bir host'a bağlamak için)

## Kurulum (bir kez)

```bash
git clone https://github.com/cuneytm/myaiprd_labs.git
cd myaiprd_labs

python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1

pip install -r requirements.txt   # hata vermeden bitmeli; mcp kurulamazsa Python sürümünü kontrol edin
cp .env.example .env               # Windows: copy .env.example .env
```

Her yeni terminal penceresinde laboratuvar komutlarından önce sanal ortamı tekrar etkinleştirin (`source .venv/bin/activate`); komut satırının başında `(.venv)` görünmelidir.

## Ayarlar: `.env`

`.env` dosyasını bir metin editörüyle açın ve kendi bilgilerinizi yazın:

```
MODEL_BASE_URL=http://localhost:11434/v1        # modelin adresi (sonu /v1)
MODEL_NAME=qwen3:8b                             # sunucudaki model adı
MODEL_API_KEY=yok                               # anahtar yoksa "yok"
WORK_DIR=/Users/kullaniciadi/Documents/lab-klasoru   # agent'ın çalışacağı klasör
```

- `WORK_DIR` için klasörün **tam yolunu** yazın. macOS'ta Finder'da klasörü Terminal penceresine sürükleyip bırakırsanız tam yol yazılır. `~/Documents/lab-klasoru` biçimi de çalışır.
- `WORK_DIR` boşsa depodaki `ornek-klasor` kullanılır.
- `.env` git'e eklenmez; API anahtarınızı başka bir dosyaya yazmayın.

## Bağlantıyı denemek

```bash
cd modul01-ai-agent
python agent.py --task "Klasörde hangi dosyalar var?"
```

İlk satırda model adını ve klasörü, ardından `[adım 1 · model önerdi] list_files(...)` satırını görüyorsanız model ve tool calling çalışıyor demektir. Sorun çıkarsa Modül 1 HOWTO.md'deki "Sorun giderme" bölümüne bakın.

---

# Claude programı laboratuvarları

myaiprd.com'daki **Claude ile Çalışmak ve Uygulama Geliştirmek** programının laboratuvarları `claude-modul01` … `claude-modul09` klasörlerindedir. Yukarıdaki iki laboratuvardan bağımsızdır: model olarak Claude API'yi kullanır.

| Modül | Klasör | Ne yapacaksınız |
| --- | --- | --- |
| 1 · Claude'u tanımak | [`claude-modul01`](claude-modul01/) | Aynı log analizini farklı modellerle ve istemlerle karşılaştıracaksınız |
| 2 · Messages API | [`claude-modul02`](claude-modul02/) | İlk API çağrısını yapıp çok turlu bir log asistanı yazacaksınız |
| 3 · Yapılandırılmış çıktı | [`claude-modul03`](claude-modul03/) | Değişiklik taleplerinden şemaya uygun JSON çıkaracak, önbelleği ölçecek, toplu işlem çalıştıracaksınız |
| 4 · Belge ve görsel | [`claude-modul04`](claude-modul04/) | Fatura PDF'lerini kontrol edecek, topoloji görselini Mermaid'e çevirecek, sözleşmeye kaynaklı soru soracaksınız |
| 5 · Tool use ve MCP | [`claude-modul05`](claude-modul05/) | Envanter araçlarıyla tool use döngüsü kuracak, aynı araçları bir MCP server'da yayınlayacaksınız |
| 6 · Agent SDK | [`claude-modul06`](claude-modul06/) | Özgeçmiş PDF'lerini işleyen, onay kapılı bir ajan yazacaksınız |
| 7 · Claude Code | [`claude-modul07`](claude-modul07/) | Switch config'lerini Claude Code ile denetleyip rapor üreteceksiniz |
| 8 · Çok adımlı ajanlar | [`claude-modul08`](claude-modul08/) | Alt ajanlı bir müşteri hizmetleri asistanını senaryolarla ve prompt injection'a karşı sınayacaksınız |
| 9 · RAG ve kapanış projesi | [`claude-modul09`](claude-modul09/) | Runbook'lar üzerinde RAG kurup uzun bağlamla karşılaştıracak ve eval ile ölçeceksiniz |

## Gerekenler

- Python 3.10 veya üstü
- Bir **Anthropic API anahtarı** ([console.anthropic.com](https://console.anthropic.com)). X
- Modül 6–8 için **Claude Code** (`npm install -g @anthropic-ai/claude-code` ya da [kurulum sayfası](https://docs.claude.com/en/docs/claude-code/setup)). Agent SDK, Claude Code'u alt süreç olarak çalıştırır.

## Kurulum

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-claude.txt
cp .env.example .env    # zaten varsa yalnızca ANTHROPIC_API_KEY satırını ekleyin
```

`.env` içinde `ANTHROPIC_API_KEY=` satırına anahtarınızı yazın. Anahtarı başka bir dosyaya ya da koda yazmayın; `.env` git'e eklenmez.

Bağlantıyı denemek için:

```bash
cd claude-modul02
python ilk_cagri.py
```

Modül 4 ve 6'daki örnek PDF'ler ve görseller depoda yoktur; o modüllerin HOWTO'sundaki ilk adım `python veri/ornek_uret.py` ile onları üretir.
