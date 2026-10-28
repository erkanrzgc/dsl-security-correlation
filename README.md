# DSL Tabanlı Güvenlik Olayı Tespit ve Korelasyon Sistemi

Suricata ağ güvenliği olayları ile Linux SSH kimlik doğrulama kayıtlarını ortak bir olay modelinde birleştiren bitirme projesi. Amaç, tespit mantığını alana özgü bir dil (DSL) ile tanımlamak ve üretilen alarmları dayanak kayıtlarla açıklamaktır.

## Mevcut durum

Proje araştırma ve tasarım aşamasındadır. Bu depo mimari yaklaşımı, DSL tasarım örneğini, geliştirme planını ve yerelde yürütülen sentetik veri ön deneyinin senaryolarını/bulgularını içerir. Çalışır güvenlik DSL ayrıştırıcısı, tespit motoru, AI entegrasyonu ve kullanıcı arayüzü henüz bu depoda bulunmamaktadır.

## Teslim kapsamı

- **Veri kaynakları:** Suricata EVE `alert`/`flow` ve Linux SSH başarısız/başarılı giriş kayıtları.
- **Analiz:** L3 IP, L4 protokol/port bilgileri ve kaynak kayıtların sunduğu seçili L7 olayları.
- **Dil ve motor:** Python/Lark, EBNF grameri, AST, anlamsal doğrulama, IR ve zaman pencereli korelasyon.
- **Beş kural türü:** alan koşulu, olay sayımı, benzersiz değer sayımı, aynı pencerede çok kaynaklı ilişkilendirme ve iki aşamalı sıralı ilişkilendirme. Türlere uygulanabilen izin listesi/istisna filtreleri.
- **Arayüz:** kural oluşturma ve test, hazır ve kullanıcı tanımlı şablonlar, alarm/kanıt inceleme ve `/help`.
- **AI desteği:** doğal dilden kural taslağı, kanıta bağlı log/alarm açıklaması ve test edilebilir yanlış pozitif filtre önerileri. Öneriler doğrulama, test ve kullanıcı onayından sonra etkinleşir.
- **Saklama ve erişim:** SQLite ve yardımcı CLI.

Temel teslim tespit ve korelasyondur. Otomatik trafik engelleme olası genişletmedir. Şifreli SSH/HTTPS içeriği çözülmez; uygulama bilgisi mevcut kaynak kayıtlarından alınır.

## Belgeler ve örnekler

| İçerik | Dosya |
|---|---|
| Bileşenler ve veri akışı | [Mimari](docs/mimari.md) |
| Dil tasarımı ve kural türleri | [DSL tasarımı](docs/dsl-tasarimi.md) |
| Örnek SSH sayım kuralı | [ssh_failures.dsl](examples/ssh_failures.dsl) |
| Yedi iş paketi | [Geliştirme planı](docs/gelistirme-plani.md) |
| Sentetik veri deneyi ve yeniden çalıştırma | [EvidenceForge ön deneyi](experiments/evidenceforge/README.md) |

DSL dosyası bir **tasarım örneğidir**; henüz çalıştırılabilir bir dil sürümü değildir. Uygulamanın kurulum ve çalıştırma adımları geliştirilen kaynaklarla birlikte eklenecektir.

## Teknik başvurular

- [Lark gramer başvurusu](https://lark-parser.readthedocs.io/en/stable/grammar.html)
- [Suricata EVE JSON biçimi](https://docs.suricata.io/en/latest/output/eve/eve-json-format.html)
- [Cisco Talos EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge)

EvidenceForge bağımsız bir üçüncü taraf araçtır. Bu depodaki ön deney onun çıktı uygunluğunu inceler; geliştirilecek sistemin tespit doğruluğunu ölçmez.
