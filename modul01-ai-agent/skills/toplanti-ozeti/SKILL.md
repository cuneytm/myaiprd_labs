---
name: toplanti-ozeti
description: Bir veya birden fazla toplantı notundan karar ve aksiyon çıkarma prosedürü. Toplantı notlarıyla ilgili isteklerde kullan.
---

# Toplantı özeti prosedürü

1. Toplantı notlarını bul (`search_files` ile "toplantı" ya da `list_files` ile notlar klasörü).
2. Her notu `read_file` ile oku.
3. Şu üç başlıkla özetle:
   - **Kararlar:** kesinleşen konular
   - **Aksiyonlar:** `kişi · iş · son tarih` (tarih yoksa "belirtilmemiş")
   - **Değişenler:** bir toplantıdan diğerine değişen tarih veya karar
4. Birden fazla not varsa en yeni notu esas al ve eskisiyle çelişen yerleri belirt.
