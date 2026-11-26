# Leaf/spine hardening kontrol listesi (kurgusal)

| # | Madde | Uygun sayılması için |
| --- | --- | --- |
| H1 | Telnet kapalı | `feature telnet` satırı yok |
| H2 | SNMP community varsayılan değil | `public` veya `private` kullanılmıyor |
| H3 | VTY erişimi ACL ile sınırlı | `line vty` altında `access-class ... in` var |
| H4 | Oturum zaman aşımı | `line vty` altında `exec-timeout` 0 değil ve 15'ten küçük veya eşit |
| H5 | En az iki NTP sunucusu | İki veya daha fazla `ntp server` satırı |
| H6 | Uzak syslog | En az bir `logging server` satırı |
| H7 | Uyarı banner'ı | `banner motd` tanımlı |
| H8 | Uplink MTU | `UPLINK` açıklamalı arayüzlerde `mtu 9216` |
