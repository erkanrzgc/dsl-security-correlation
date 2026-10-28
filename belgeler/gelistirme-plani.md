# Geliştirme planı

| Paket | İş ve çıktı |
|---|---|
| P1 | Gereksinimler, literatür, ortak olay/dil sözleşmesi, arayüz akışları ve kabul ölçütleri |
| P2 | Sentetik senaryoların düzeltilmesi, Suricata/SSH laboratuvarı, adaptörler ve etiketli örnekler |
| P3 | EBNF, Lark ayrıştırıcısı, AST, anlamsal doğrulama ve IR |
| P4 | Beş kural türü, zaman penceresi/korelasyon motoru, SQLite ve yardımcı CLI |
| P5 | Arayüz, hazır/özel şablon yönetimi, alarm/kanıt ekranları ve yardım |
| P6 | AI ile DSL taslağı, kanıta bağlı açıklama ve filtre önerilerinin entegrasyonu |
| P7 | Uçtan uca test, değerlendirme, düzeltmeler, kurulum/kullanım belgeleri ve sunum |

P2 ve P3 ortak sözleşmeler üzerinden paralel ilerler. Motor, adaptör ve doğrulanmış IR çıktılarıyla geliştirilir. Arayüz ve AI, modül arayüzleri netleştikten sonra ara çıktılarla bütünleştirilir.

## Değerlendirme

- Dil: geçerli/geçersiz kurallar, hata konumları ve alan/parametre doğrulaması.
- Motor: eşik/pencere sınırları, IP/hedef grubu ayrımı, tekrarlar, benzersiz portlar, eksik kaynak, doğru/ters sıra ve zaman aşımı.
- Arayüz: kural/şablon/test/alarm akışları ve yardım örnekleri.
- AI: geçerli ve senaryoya uygun kural üretimi, açıklamaların kayıtlarla uyumu ve yanıt süresi.
- Sonuçlar: senaryo düzeyinde yanlış pozitif/negatif, precision, recall ve alarm gecikmesi.

Filtre ayarlama ve son değerlendirme verisi ayrı tutulur. Başlangıç ve öneri sonrası kurallar aynı etiketli değerlendirme verisinde karşılaştırılır. Yanlış alarmların azalmasıyla birlikte kaçırılan saldırılar da raporlanır. AI'nin yorumu gerçek etiket yerine kullanılmaz.
