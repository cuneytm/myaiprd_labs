# Claude modül 4 · Ne yapacaksınız

```bash
cd claude-modul04
python veri/ornek_uret.py
```

## Adım 1 · Önce kodsuz

`veri/faturalar/fatura-2.pdf`'i claude.ai'de bir sohbete yükleyip "kalemleri tablo yap ve toplamları kontrol et" deyin. Sonucu not edin.

## Adım 2 · Fatura çıkarımı

`fatura.py`'deki üç TODO'yu tamamlayın, sonra:

```bash
python fatura.py veri/faturalar/*.pdf
```

**Gözlemleyin:** Hangi faturada toplam kontrolü başarısız oldu? Claude yanlış toplamı "düzeltti" mi, yoksa belgede yazdığı gibi mi aktardı? (Prompt'ta "düzeltme" dedik; neden önemli?)

## Adım 3 · Topoloji

```bash
python topoloji.py veri/topoloji.png
```

Üretilen `topoloji.mmd` içeriğini claude.ai'de "bunu Mermaid diyagramı olarak çiz" diyerek bir Artifact'e dönüştürün ve orijinal görselle karşılaştırın. Eksik veya fazla bağlantı var mı?

## Adım 4 · Kaynaklı cevap

```bash
python sozlesme_soru.py "Yedek parça teslim süresi nedir?"
python sozlesme_soru.py "SLA uyumu düşerse ne olur?"
python sozlesme_soru.py "Sözleşmede ceza puanı sistemi var mı?"
```

İlk çalıştırmada dosya Files API'ye yüklenir, id `.sozlesme_file_id`'ye yazılır; sonraki sorularda dosya tekrar gönderilmez.

**Gözlemleyin:** Her cümlenin yanındaki kaynak doğru sayfayı gösteriyor mu? Sözleşmede olmayan bir şey sorduğunuzda ne oldu?

## Alıştırma

`fatura.py`'yi Batch API ile çalışacak şekilde değiştirin (modül 3'teki `toplu.py`'ye bakın).
