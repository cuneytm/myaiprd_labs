# AI Agent ve MCP laboratuvarları

AI agent'ların ve Model Context Protocol'ün (MCP) temellerini uygulamalı olarak gösteren iki laboratuvar. Kod kısadır ve framework kullanılmaz: agent döngüsünü ve MCP'yi doğrudan görürsünüz. Her dosyanın başında hangi kavramı gösterdiği yazar.

Her iki laboratuvarda da agent, **sizin seçtiğiniz bir klasör** üzerinde sizin verdiğiniz işleri yapar: dosyaları listeler, okur, arar, özetler ve isterseniz yeni dosya yazar.

| Modül | Klasör | Ne yapacaksınız |
| --- | --- | --- |
| 1 · AI Agent | [`modul01-ai-agent`](modul01-ai-agent/) | Instructions, tools, skills, memory ve loop'tan oluşan basit bir agent'ı çalıştırıp inceleyeceksiniz. Dosya işlemleri agent'ın kendi kodundaki tool'larla yapılır |
| 2 · MCP | [`modul02-mcp`](modul02-mcp/) | Aynı dosya işlemlerini bir MCP server'da tool olarak yayınlayacak, önce modelsiz bir client'la, sonra agent'la kullanacaksınız |

Her modülde iki dosya vardır: **README.md** ne öğreneceğinizi ve hangi kavramın hangi dosyada olduğunu anlatır; **HOWTO.md** adım adım ne yapacağınızı ve alıştırmaları verir.

## Gerekenler

- **Python 3.10 veya üstü** (`python3 --version`)
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

pip install -r requirements.txt
cp .env.example .env               # Windows: copy .env.example .env
```

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
