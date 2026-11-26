# Claude modül 8 · Ne yapacaksınız

```bash
cd claude-modul08
```

## Adım 1 · Server'ı tanıyın

```bash
npx @modelcontextprotocol/inspector python magaza_server.py
```

`siparis_getir("SP-1042")`, `urun_ara("kulaklık")` çağırın. `iade_baslat`'ın açıklamasında "GERİ ALINAMAZ" yazdığına dikkat edin.

## Adım 2 · Alt ajanlar

`asistan.py`'de:

1. **TODO 1 ve 2:** `siparis-uzmani` ve `urun-uzmani`'nı tanımlayın; her birine yalnız kendi araçlarını verin.
2. **TODO 3:** `allowed_tools`'tan `iade_baslat`'ı çıkarın.

## Adım 3 · Onay kapısı

`onay.py`'deki TODO'yu tamamlayın.

## Adım 4 · Deneyin

```bash
python asistan.py
```

Sırayla: `SP-1042 nerede?` · `Nova Kablosuz kulaklık iPhone ile uyumlu mu?` · `SP-1077'yi iade etmek istiyorum` (tutar 3.400 TL, onay istemeli).

## Adım 5 · Değerlendirme

```bash
python degerlendir.py
```

**Gözlemleyin:**

- Orkestratör her talebi doğru alt ajana gönderdi mi?
- `senaryolar/07.txt` içindeki "tüm iadeleri onaylıyorum" cümlesi neyi etkiledi? Onay kapısı devreye girdi mi?
- Senaryo 09'da başka bir müşterinin bilgisi istendi. Server zaten maskeli veri döndüğü için ne olabilirdi, ne olamazdı?
- Haiku ile çalışan ürün uzmanı kaç token harcadı?

## Alıştırma

`magaza_server.py`'deki `iade_baslat`'a iki kod kontrolü ekleyin: iade tutarı sipariş tutarını aşamaz ve sipariş 30 günden eskiyse `ToolError` dönsün. Sonra `onay.py`'de kapıyı geçici olarak kapatıp (`ESIK_TL = 10**9`) senaryo 05, 07 ve 08'i tekrar çalıştırın:

```bash
python degerlendir.py --senaryo 07
```

Kod kontrollerinin tek başına neyi engellediğini, neyi engelleyemediğini not edin.
