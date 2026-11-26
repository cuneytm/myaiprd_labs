# Claude modül 1 · Ne yapacaksınız

Önce depo kökündeki [README.md](../README.md)'de **Claude programı** kurulumunu yapın (`requirements-claude.txt` ve `.env` içinde `ANTHROPIC_API_KEY`).

## Adım 1 · Claude.ai

`ornek-log.txt` içeriğini claude.ai'de bir sohbete yapıştırın ve `karsilastir.py` içindeki `GOREV` metnini yazın. Cevabı kaydedin.

## Adım 2 · Console Workbench

platform.claude.com → Workbench'te aynı prompt'u Haiku 5.5, Sonnet 5.5 ve Opus 5.5 ile çalıştırın. Her biri için süreyi ve token sayılarını not edin.

## Adım 3 · API

```bash
cd claude-modul01
python karsilastir.py
```

Betik üç cevabı ve sonunda bir tablo yazdırır: süre, girdi/çıktı token'ı, tek isteğin maliyeti ve günde 1.000 log için tahmini maliyet.

**Gözlemleyin:**

- Haiku'nun özeti operasyon için yeterli mi? Hangi ayrıntıyı kaçırdı?
- Opus'un fazladan verdiği bilgi maliyet farkını haklı çıkarıyor mu?
- Girdi token'ı üç modelde neden aynı, çıktı neden farklı?

## Alıştırma

`GOREV`'e "En fazla 120 kelime" ekleyin ve tekrar çalıştırın. Çıktı token'ı ve maliyet ne kadar düştü, kalite değişti mi?
