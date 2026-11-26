# Claude modül 5 · Ne yapacaksınız

```bash
cd claude-modul05
```

## Adım 1 · Döngüyü siz yazın

`dongu.py`'deki üç TODO'yu tamamlayın, sonra:

```bash
python dongu.py "DC1'de out-of-sync leaf'lerin config farkını göster"
```

**Gözlemleyin:** Kaç tur sürdü? İkinci turda iki `config_farki` çağrısı aynı anda (paralel) geldi mi?

Aynı soruyu `python runner.py` ile çalıştırın: döngüyü SDK yürütür, sonuç aynıdır.

## Adım 2 · Hata mesajının etkisi

```bash
python dongu.py "DC3 fabric'inde kaç switch var?"
```

`araclar.py`'deki `switch_durumu` bilerek kötü bir hata veriyor (`"bulunamadı"`). Mesajı "DC3-FABRIC için kayıt yok. Bilinen fabric'ler: DC1-FABRIC, DC2-FABRIC." gibi yol gösteren bir metinle değiştirip tekrar çalıştırın. Claude nasıl toparlandı?

## Adım 3 · MCP server

`envanter_server.py`'deki iki TODO'yu tamamlayın ve araçları modelsiz deneyin:

```bash
npx @modelcontextprotocol/inspector python envanter_server.py
```

Inspector'da Tools sekmesinde araçları elle çağırın, Resources sekmesinde `envanter://ozet`'i okuyun.

## Adım 4 · Claude Code'a bağlayın

```bash
claude mcp add envanter -- python "$(pwd)/envanter_server.py"
claude
```

Oturumda `/mcp` ile bağlantıyı görün ve "DC1'de out-of-sync switch var mı, farkları ne?" diye sorun.

## Adım 5 · Kendi uygulamanızdan

```bash
python api_istemci.py "DC1'de kaç leaf var?"
```

## Alıştırma

"DC1'deki tüm leaf'lerin yıllık lisans maliyeti kaç TL?" sorusunu `dongu.py` ile sorun. `LISANS_USD` verisini döndüren bir `lisans_bedeli` aracı ekleyip Claude'un `doviz_kuru` ile birlikte kullanmasını sağlayın.
