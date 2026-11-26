# Claude modül 7 · Ne yapacaksınız

Bu klasörü depodan ayrı bir çalışma kopyasına alın ki Claude Code'un yaptığı değişiklikleri kendi git geçmişinizde izleyebilin:

```bash
cp -r claude-modul07 ~/lab07 && cd ~/lab07
git init && git add -A && git commit -m "başlangıç"
claude
```

## Adım 1 · CLAUDE.md

Oturumda `/init` çalıştırın. Oluşan `CLAUDE.md`'yi okuyun ve şu kuralları ekletin (veya kendiniz ekleyin):

- `configs/` altındaki dosyalar salt okunurdur, asla değiştirilmez.
- Üretilen raporlar `rapor/` altına yazılır.
- Test komutu: `python -m pytest -q`

## Adım 2 · Plan modu ile araç

`Shift+Tab` ile plan moduna geçin ve şunu yazın:

> `cfgdiff.py` adında, iki NX-OS config dosyasını bölüm bölüm (hostname, vlan, interface, bgp, acl, diğer) karşılaştıran bir CLI aracı yazacağız. Yalnız sıra farkı olan satırları fark sayma. Çıktı `beklenen/` klasöründeki örneklere benzesin. Önce klasörü incele ve plan çıkar.

Planı okuyun, gerekirse düzeltin, sonra normal moda geçip uygulatın.

## Adım 3 · Test

> `beklenen/` klasöründeki üç örneği kullanarak pytest testleri yaz ve çalıştır. Testler geçene kadar düzelt.

**İpucu:** Claude'dan çıktıyı size de göstermesini isteyin: `!python cfgdiff.py configs/leaf-101.cfg configs/leaf-104.cfg`

## Adım 4 · Skill

`.claude/skills/config-denetim/SKILL.md` dosyasını portal Bölüm 7.4'teki örnekten oluşturun (`kontrol_listesi.md`'yi okusun, sonucu `rapor/denetim-<tarih>.md`'ye tablo olarak yazsın). Sonra:

```text
/config-denetim configs/leaf-*.cfg
```

**Beklenen:** LEAF-104 H1, H2, H3, H4 ve H7'de; LEAF-103 H5 ve H8'de uygun değil.

## Adım 5 · Hook

Portal Bölüm 7.5'teki `configs_koru.py` hook'unu `.claude/hooks/` altına ve `.claude/settings.json`'a ekleyin. Claude Code'u yeniden başlatın (`/exit`, `claude`) ve bilerek isteyin:

> leaf-103.cfg'deki eksik NTP satırlarını ekle.

Hook düzenlemeyi engellemeli; Claude değişikliği `rapor/` altına bir öneri olarak yazmalı.

## Adım 6 · Git ve geri alma

Değişiklikleri `git commit` ile kaydedin. Sonra Claude'dan `cfgdiff.py`'de bir değişiklik isteyin, beğenmeyin ve `Esc Esc` (veya `/rewind`) ile geri dönün.

**Gözlemleyin:**

- Plan modunda Claude hangi dosyaları okudu, planı hangi varsayımlarla kurdu?
- Hook engellediğinde Claude nasıl tepki verdi?
- `CLAUDE.md`'deki "configs salt okunur" kuralını silip yalnız hook'a güvendiğinizde davranış değişti mi?

## Alıştırma

Bölüm 7.6'daki `log-analisti` subagent'ını `.claude/agents/` altına ekleyin ve `logs/` klasörünü ona inceletin. Sonra aynı işi etkileşimsiz çalıştırın:

```bash
claude -p "logs/ klasöründeki olayları cihaz bazında özetle, güvenlik açısından şüpheli olanları ayrıca listele" \
  --allowedTools "Read,Grep,Glob" --output-format json > rapor/log-ozet.json
```
