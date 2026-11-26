# DC1 değişiklik yönetimi runbook'u (kurgusal)

Bu runbook, DC1 veri merkezindeki VXLAN EVPN fabric'inde yapılan değişikliklerin nasıl sınıflandırılacağını, hangi onayların gerektiğini ve hangi kontrollerin yapılacağını tanımlar. Değişiklik talebi analiz eden asistan bu belgeye göre karar verir.

## 1. Kapsam

Fabric iki spine (SPINE-01, SPINE-02), on iki leaf (LEAF-101 ... LEAF-112) ve iki border leaf'ten (BORDER-01, BORDER-02) oluşur. Leaf'ler vPC çiftleri halinde çalışır: 101-102, 103-104, 105-106, 107-108, 109-110, 111-112. Border leaf'ler internet ve WAN bağlantılarını taşır. Underlay OSPF, overlay BGP EVPN'dir. Tüm konfigürasyon NDFC üzerinden yönetilir; cihaza doğrudan CLI ile yapılan değişiklik "out-of-band" sayılır ve olay kaydı gerektirir.

## 2. Değişiklik türleri

### 2.1 Standart değişiklik

Önceden onaylanmış, düşük riskli, tekrar eden işler. Bakım penceresi gerekmez, mesai içinde yapılabilir. Örnekler:

- Yeni VLAN tanımlamak ve henüz trafik taşımayan bir trunk'a eklemek
- VLAN veya interface açıklamasını (description) değiştirmek
- Kullanılmayan bir erişim portunu yeni bir sunucuya atamak
- SNMP, syslog veya NTP sunucusu eklemek (mevcutları silmeden)

### 2.2 Normal değişiklik

Değişiklik danışma kurulu (CAB) onayı gerekir. Bakım penceresinde yapılır. Örnekler:

- Üretim trafiği taşıyan bir portun VLAN'ını değiştirmek
- vPC allowed VLAN listesini değiştirmek
- BGP route-map, prefix-list veya community politikalarını değiştirmek
- Bir VLAN'ı kaldırmak (bağlı uç kalmadığı doğrulanmış olsa bile)
- Border leaf'lerde yapılan her değişiklik

### 2.3 Acil değişiklik

Üretimi etkileyen bir olayı düzeltmek için yapılır. Vardiya yöneticisinin sözlü onayı yeterlidir, CAB'a sonradan bildirilir. Olay kaydı numarası olmadan acil değişiklik yapılamaz.

## 3. Risk sınıflandırması

| Risk | Tanım | Örnek |
| --- | --- | --- |
| düşük | Trafik kesintisi beklenmez, geri alma tek komut | Yeni VLAN, açıklama değişikliği |
| orta | Tek sunucu veya tek müşteri için kısa kesinti olabilir | Üretimdeki portun VLAN değişikliği |
| yüksek | Birden fazla müşteri, routing veya border etkilenir | Route-map, vPC allowed list, border değişikliği |

Belirsizlik varsa bir üst risk seviyesi seçilir.

## 4. Bakım penceresi

- Normal pencere: Salı ve Perşembe 01:00–05:00
- Hafta sonu penceresi: Cumartesi 00:00–06:00, yalnız yüksek riskli değişiklikler için
- Standart değişiklikler için pencere gerekmez
- Müşteri "gece yapılsın" dese bile standart değişiklik pencere gerektirmez; ama müşteri isteği not edilir

## 5. VLAN kuralları

- Geçerli VLAN aralığı 1–4094'tür. 1, 1002–1005 ve 3967–4094 aralığı rezervedir ve müşteriye atanamaz.
- Müşteri VLAN'ları 100–3966 aralığından verilir.
- Her VLAN'ın adı `MUSTERI-AMAC` biçiminde olmalıdır (ör. `ATLAS-PROD`).
- Bir VLAN birden fazla vPC çiftinde kullanılıyorsa değişiklik her çift için ayrı satır olarak kaydedilir.

## 6. Ön kontroller

Her değişiklikten önce:

1. NDFC'de ilgili cihazların "In-Sync" olduğunu doğrulayın.
2. Değişiklikten etkilenecek portların ve VLAN'ların güncel durumunu kaydedin (`show vlan brief`, `show interface status`, `show vpc`).
3. Geri alma (rollback) adımlarını talep kaydına yazın.
4. Border leaf değişikliklerinde BGP komşuluk durumunu ve alınan prefix sayılarını kaydedin.

## 7. Son kontroller

1. NDFC'de deploy sonrası tüm cihazların "In-Sync" olduğunu doğrulayın.
2. Etkilenen sunucu sahiplerinden bağlantı testi isteyin.
3. Monitoring sisteminde 15 dakika boyunca yeni alarm olmadığını doğrulayın.
4. Talep kaydını kapatırken uygulanan komutları ve kontrol çıktılarını ekleyin.

## 8. Sık karşılaşılan durumlar

### 8.1 "Sadece isim değişikliği"

VLAN adı değişikliği standart değişikliktir, risk düşüktür. Ancak monitoring sistemi VLAN adına göre gruplama yapıyorsa izleme ekibine haber verilir.

### 8.2 "Sunucu taşındı, VLAN'ı kaldırın"

VLAN kaldırmak normal değişikliktir. Kaldırmadan önce `show mac address-table vlan X` ile VLAN'da öğrenilmiş MAC kalmadığı doğrulanır. MAC varsa talep sahibine geri dönülür.

### 8.3 Talepte cihaz adı belirsiz

"Leaf'lere ekleyin" gibi belirsiz taleplerde hangi cihazların etkileneceği talep sahibine sorulur; asistan cihaz uydurmaz, `cihaz` alanına talepte geçen en açık ifadeyi yazar ve özetinde belirsizliği belirtir.

### 8.4 VLAN numarası kurallara uymuyor

Talepteki VLAN numarası geçerli aralığın dışında veya rezerve aralıktaysa asistan numarayı değiştirmez; olduğu gibi aktarır ve özetinde sorunu belirtir. Doğrulama katmanı bu talebi insana yönlendirir.

## 9. İletişim

- Ağ operasyon vardiyası: dahili 4100
- Değişiklik danışma kurulu: her Salı 14:00
- Acil durum: vardiya yöneticisi, dahili 4199
