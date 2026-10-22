# Modül 1 · Nasıl çalışır, ne yapacaksınız

Önce depo kökündeki [README.md](../README.md)'deki kurulumu yapın: sanal ortam, `pip install`, `.env` (model bilgileri ve `WORK_DIR`). Sonra:

```bash
cd modul01-ai-agent
```

Agent her başladığında hangi modeli ve hangi klasörü kullandığını yazar. Çalışırken de içeride olanları gösterir:

```
  [adım 1 · model önerdi] list_files({"path": "."})        <- modelin önerisi
  [adım 1 · sonuç] README.txt | [klasör] notlar | ...       <- harness'ın çalıştırdığı tool'un sonucu
```

Bu satırları takip edin: agent'ın nasıl karar verdiğini görmenin yolu budur. Aşağıdaki örnekler `ornek-klasor` içindir; kendi klasörünüzü verdiyseniz soruları ona göre uyarlayın.

---

## Adım 1 · İlk görev: tool calling ve döngü

```bash
python agent.py --task "Klasörde hangi dosyalar var?"
```

**Gözlemleyin:** Model önce `list_files` önerir; harness çalıştırır; sonuç context'e eklenir; model ikinci çağrıda cevabı yazar. İki model çağrısı ve bir tool çağrısı: döngünün en kısa hali.

Sonra `tools.py`'yi açın: modelin bu tool hakkında bildiği tek şey `description` ve `parameters` alanlarıdır.

**Context'e bakın:** `memory/son-gorev-context.json` dosyasını açın. Modele giden her şey buradadır: `system` mesajı (instructions + skill kataloğu + uzun dönem bellek), sizin göreviniz (`user`), modelin tool önerisi (`assistant` + `tool_calls`), tool sonucu (`tool`) ve son cevap. Bu liste görevin **short-term memory**'sidir; görev bitince silinir, dosya yalnız incelemeniz için yazılır.

## Adım 2 · Birden fazla adım: model yolu kendisi bulur

```bash
python agent.py --task "Yapılacaklar listesinde bitmemiş işler hangileri ve toplantı notlarına göre kimin sorumluluğunda?"
```

**Gözlemleyin:** Hangi dosyaları, hangi sırayla okuyacağını kimse söylemedi. Model önce listeleyebilir ya da arayabilir, sonra okuduklarına göre sonraki adıma karar verir. Aynı görevi iki kez çalıştırın: adımlar aynı mı?

## Adım 3 · Skill: prosedürü model kendisi yükler

```bash
python agent.py --task "Toplantılarda neler kararlaştırıldı?"
```

**Gözlemleyin:**
- Model önce `load_skill("toplanti-ozeti")` çağırıyor mu? Context'te yalnız skill kataloğu var (`system_prompt()` fonksiyonuna bakın); tam talimatı model ister.
- Cevap skill'deki biçimde mi: **Kararlar**, **Aksiyonlar**, **Değişenler**?

Model skill'i yüklemeden de cevap verebilir. Skill bir **yöntemdir**; modele nasıl yapacağını öğretir, zorlamaz.

## Adım 4 · Dosya yazmak

```bash
python agent.py --task "Klasör için bir rapor hazırla ve RAPOR.md olarak kaydet."
```

**Gözlemleyin:** Model `klasor-raporu` skill'ini yükleyip adımlarını izliyor mu? En sonda `write_file` çağrılır ve `RAPOR.md` çalışma klasörünüzde oluşur. Dosyayı açıp bakın.

## Adım 5 · Sohbet ve memory

```bash
python agent.py
```

Sırayla yazın:

```
Siz> Özetleri her zaman madde madde isterim, bunu hatırla.
Siz> Proje planında hangi aşamalar var?
Siz> Bunlardan hangisi henüz başlamadı?
Siz> q
```

**Gözlemleyin:**
- İlk mesajda model `remember` tool'unu çağırır. `memory/facts.md` dosyasını açın: bu **long-term memory**'dir ve her yeni görevde context'e konur.
- Üçüncü mesajdaki "bunlardan" kelimesini model anlar, çünkü önceki mesajlar `messages` listesindedir (**short-term memory**). Model kendisi hiçbir şey hatırlamaz: harness her çağrıda bütün listeyi yeniden gönderir.

Şimdi oturumu geri yükleyin:

```bash
python agent.py --resume
Siz> Az önce hangi dosyadan bahsettik?
```

`memory/session.json` yüklendiği için cevap verebilir (**session memory**). Aynı soruyu `--resume` olmadan sorun ve farkı görün.

### Hangi bellek ne zaman yazılır?

| Bellek | Dosya | Ne zaman yazılır | Sonraki görevde modele gider mi? |
| --- | --- | --- | --- |
| Short-term | yok (bellekte); kopyası `son-gorev-context.json` | Her görevde; görev bitince silinir | Hayır |
| Session | `session.json` | Yalnız sohbet modunda (`python agent.py`), her mesajdan sonra | Yalnız `--resume` ile |
| Long-term | `facts.md` | Yalnız model `remember` tool'unu çağırdığında | Evet, her görevde |
| Görev kuyruğu sonuçları | `kuyruk-....md` | Yalnız `--tasks` ile | Hayır |

Yani `--task "1.1.1.1 geçen dosya var mı?"` gibi tek seferlik bir soru `facts.md`'ye yazılmaz: instructions modele yalnız **kalıcı** bilgileri kaydetmesini söyler ve bu kararı model verir. Neyin belleğe yazılacağına karar vermek de agent tasarımının bir parçasıdır.

## Adım 6 · Dış döngü: görev kuyruğu

```bash
python agent.py --tasks tasks.txt
```

**Gözlemleyin:** Her görev kendi iç döngüsünde ve **temiz bir context** ile çalışır; bir görevin mesajları diğerine taşınmaz. Sonuçlar `memory/kuyruk-....md` dosyasına yazılır. Gerçek hayatta kuyruk bir zamanlayıcıdan, e-postadan ya da bir mesajlaşma kanalından dolabilir; agent aynı kalır.

`tasks.txt` dosyasına kendi görevlerinizi ekleyip tekrar çalıştırın.

## Adım 7 · Workflow ile karşılaştırma

```bash
python workflow.py
```

**Gözlemleyin:** Hangi dosyaların okunacağı ve sıra kodda sabittir; model yalnız son adımda özet yazar, tool seçmez. Her çalıştırmada aynı yol izlenir. Agent'ta ise yolu model seçiyordu.

---

## Alıştırmalar

1. **Yeni tool:** `tools.py`'ye bir dosyanın boyutunu ve son değiştirilme tarihini döndüren `file_info(path)` tool'u ekleyin (`f.stat().st_size`, `f.stat().st_mtime`). Fonksiyonu yazın ve `TOOLS` sözlüğüne kaydedin. Agent'a "en son hangi dosya değişti?" diye sorun. `agent.py`'de bir değişiklik gerekti mi?
2. **Instructions'ın etkisi:** `instructions.md`'ye "Her cevabın sonuna hangi dosyaları okuduğunu liste olarak ekle." satırını ekleyin ve Adım 2'yi tekrarlayın.
3. **Yeni skill:** `skills/` altında `butce-analizi/SKILL.md` oluşturun. Frontmatter'da `name` ve `description` zorunlu; gövdede bir CSV bütçe dosyasının nasıl yorumlanacağını adım adım yazın (planlanan ile gerçekleşeni karşılaştır, aşan kalemleri belirt). Agent'a "bütçede sorun var mı?" diye sorun. Model skill'inizi buluyor mu?
4. **Açıklamanın gücü:** `search_files` tool'unun `description` alanını "Arama yapar." olarak kısaltın. Adım 2'deki görevde model hâlâ bu tool'u kullanıyor mu?
5. **Model değiştirmek:** `.env`'de başka bir model deneyin (daha küçük ya da daha büyük). Tool seçimi, skill kullanımı ve adım sayısı nasıl değişiyor?
6. **Adım sınırı:** `.env`'de `MAX_STEPS=2` yapıp Adım 4'ü tekrarlayın. Ne oluyor? Değeri geri alın.

## Tartışma soruları

- `write_file` tool'unu çağıran kim: model mi, harness mı?
- Model aynı göreve neden her seferinde aynı adımlarla gitmeyebilir? Bu bir sorun mu?
- Uzun dönem belleğe (`facts.md`) her şeyi yazmak neden iyi bir fikir değildir?
- Bir işi ne zaman agent, ne zaman workflow olarak yaparsınız?

## Sorun giderme

| Belirti | Neden ve çözüm |
| --- | --- |
| `Connection refused` / `Connection error` | Model sunucusu çalışmıyor ya da `MODEL_BASE_URL` yanlış. Ollama için uygulamanın açık olduğundan emin olun; adres `http://localhost:11434/v1` |
| `model "..." not found` | `MODEL_NAME` sunucudaki adla aynı değil. Ollama'da `ollama list` |
| `does not support tools` | Model tool calling desteklemiyor. Tool destekleyen bir model seçin (ör. qwen3, llama3.1) |
| Model tool çağırmadan uyduruyor | Küçük modellerde olur. Daha büyük bir model deneyin ya da görevi daha açık yazın ("dosyaları listele, sonra ...") |
| Agent başka bir klasörde çalışıyor | Başlangıçta yazan `Klasör:` satırına bakın. `.env`'deki `WORK_DIR` tam yol olmalı |
| `... çalışma klasörünün dışında` | Tool'lar yalnız `WORK_DIR` içinde çalışır; yolları klasöre göre göreli verin |
| Cevap çok yavaş | Model CPU'da ya da bellek sınırında çalışıyor olabilir. Daha küçük bir model seçin |
| `401 Unauthorized` | `MODEL_API_KEY` yanlış ya da eksik |
