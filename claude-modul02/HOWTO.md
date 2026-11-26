# Claude modül 2 · Ne yapacaksınız

```bash
cd claude-modul02
python ilk_cagri.py
```

Bağlantı çalışıyorsa cevap ve altında `stop_reason` ile `usage` görünür. `401` alıyorsanız `.env`'deki `ANTHROPIC_API_KEY`'i kontrol edin.

## Adım 1 · TODO'ları tamamlayın

`asistan.py`'de:

1. **TODO 1:** Claude'un cevabını `gecmis`'e ekleyin.
2. **TODO 2:** Cevabı `client.messages.stream` ile geldikçe yazdırın.
3. **TODO 3:** `anthropic.RateLimitError`'u ayrı yakalayın.

## Adım 2 · Çalıştırın

```bash
python asistan.py --log ornek-loglar/bgp-flap.log
```

Üç soru sorun, örneğin: "Ne oluyor?", "Flap'ler ne sıklıkla?", "CRC hatalarıyla ilişkisi var mı?"

**Gözlemleyin:**

- Her turda `usage` girdisi neden büyüyor? (Geçmişin tamamı her istekte gidiyor.)
- TODO 1'i yapmadan önce ikinci soruda ne oldu?
- Streaming ile ilk kelimenin ekrana gelme süresi değişti mi?

## Alıştırma

`max_tokens`'ı 60'a düşürün. `stop_reason` ne oldu? Kesilen cevabı kullanıcıya nasıl belirtirsiniz?
