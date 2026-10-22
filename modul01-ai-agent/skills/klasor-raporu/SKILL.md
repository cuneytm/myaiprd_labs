---
name: klasor-raporu
description: Çalışma klasörünün genel bir raporunu hazırlama prosedürü. "rapor", "klasörde neler var", "özet çıkar" gibi isteklerde kullan.
---

# Klasör raporu prosedürü

1. `list_files` ile klasörü ve alt klasörlerini listele (alt klasörler için `list_files` tekrar çağrılır).
2. Dosyaları uzantısına göre grupla ve say.
3. En fazla 5 önemli dosyayı `read_file` ile oku ve her biri için tek cümlelik özet yaz.
4. Raporu şu biçimde hazırla:

```
# Klasör raporu
## Genel bakış
<dosya sayısı, türlere göre dağılım>
## Önemli dosyalar
- <yol>: <tek cümle özet>
## Dikkat edilecekler
<varsa tarihler, tamamlanmamış işler, tutarsızlıklar>
```

5. Kullanıcı kaydetmeni istediyse `write_file` ile kaydet; istemediyse yalnız ekrana yaz.
