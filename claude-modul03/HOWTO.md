# Claude modül 3 · Ne yapacaksınız

```bash
cd claude-modul03
```

## Adım 1 · Çıkarıcı

`cikarici.py`'de iki TODO var:

1. **TODO 1:** `kurallari_denetle`'ye VLAN aralığı kurallarını ekleyin (runbook bölüm 5).
2. **TODO 2:** Kural ihlalinde hatayı Claude'a açıklamasıyla geri verip tekrar isteyin.

```bash
python cikarici.py veri/talepler.jsonl --ilk 10
python cikarici.py veri/talepler.jsonl --ilk 50     # 5 hatalı VLAN'ı da görmek için
```

**Gözlemleyin:** Geçersiz JSON hiç geldi mi? Hatalı VLAN'lı talepler kaç denemede ne oldu? Claude VLAN numarasını "düzeltmeye" çalıştı mı, yoksa olduğu gibi bırakıp özetinde mi belirtti?

## Adım 2 · Önbellek

```bash
python onbellek_olc.py
python onbellek_olc.py --boz
```

İlk istekte `cache yazma`, sonrakilerde `cache okuma` dolmalı. `--boz` ile her istekte system prompt'un ilk satırı değiştiği için önbellek hiç tutmaz.

## Adım 3 · Batch

```bash
python toplu.py
```

Batch genellikle birkaç dakikada, en geç 24 saatte biter. Betiği kapatırsanız yazdırılan id ile `python toplu.py --id msgbatch_...` diyerek sonuçları sonra alabilirsiniz.

**Gözlemleyin:** Sonuçlar hangi sırayla geldi? Toplam maliyet normal çağrıya göre ne kadar?

## Alıştırma

`cikarici.py`'de `MODEL`'i `claude-haiku-5-5` yapın ve 50 talepte Sonnet ile aynı `risk` değerini kaç kez verdiğini sayın.
