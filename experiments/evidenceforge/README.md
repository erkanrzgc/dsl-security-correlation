# EvidenceForge sentetik veri ön deneyi

Bu deney, Cisco Talos [EvidenceForge](https://github.com/Cisco-Talos/EvidenceForge) çıktısının proje senaryolarına uygunluğunu inceler. Gerçek ağa saldırı gönderilmemiştir. Çıktılar Linux syslog, Zeek ve metin tabanlı IDS kayıtlarıdır; Suricata EVE değildir.

## Kaynak ve senaryolar

- Üretici: EvidenceForge 2.1.2, commit `79fcfcdf3726168dacfede5a27aab2aa7a2f3d69`.
- Başlangıç senaryosu: [scenario.yaml](scenario.yaml), ayrı başarısız giriş olayları.
- Revize senaryo: [scenario-bulk.yaml](scenario-bulk.yaml), sabit aralıklarla beş başarısız giriş.
- Kurgusal ortam: bir kullanıcı, iki Ubuntu sistem, ağ ve IDS sensörleri; bir saatlik olay aralığı.
- Rastgelelik başlangıç değeri: `20261028`.
- Yerel ön deney bulguları: [observed-results.json](observed-results.json).

JSON dosyası önceki yerel çalıştırmanın gözlemidir; yeni ortamda ölçüm yapılmadan aynı sonucun alındığı varsayılmamalıdır. Üretilmiş veri demetleri ve üçüncü taraf araç kaynakları bu depoya eklenmemiştir.

## Gözlenen sonuçlar

| Kontrol | Başlangıç | Revize |
|---|---|---|
| Veri dosyası / satır | 10 / 433 | 9 / 389 |
| Senaryo IP'sinden SSH başarısızlığı | 3 | 5 |
| 60 saniyedeki en yüksek başarısızlık | 2 | 5 |
| Senaryo IP'sinden başarılı SSH girişi | 1 | 1 |
| Ortak IP/sunucu bağlamında SSH ve IDS | Bulundu | Bulundu |
| Gözlenen tarama hedefindeki farklı port | 20 | 20 |
| Amaçlanan SSH sunucusundaki tarama portu | 0 | 0 |
| EVE JSON dosyası | 0 | 0 |
| Üreticinin zorunlu kabul sonucu | FAIL | FAIL |

Başlangıç senaryosunun 10 veri dosyası iki çalıştırmada birebir eşleşmiştir. Revize senaryo için ikinci üretim karşılaştırması yapılmamıştır. İlk senaryoda olay görünürlüğü, ilişkilendirilebilirlik ve zaman bütünlüğü; revize senaryoda anlatı iz kapsamı zorunlu kabul ölçütleri geçmemiştir.

Üreticinin işlem çıkış kodu tek başına kabul sonucu değildir; `Acceptance` satırı ayrıca okunmalıdır. Genel kalite puanı, bu projenin tespit doğruluğu değildir.

## Yeniden çalıştırma

Aşağıdaki PowerShell komutları bu klasörde çalıştırılır. Git, Python 3.12 ve uv gerekir. Üreticinin kendi lisans ve kurulum koşulları geçerlidir. Windows üzerinde üreticinin özel spool dizini/NTFS izin koşulları ayrıca sağlanmalıdır; gerekiyorsa `EFORGE_SPOOL_DIR` bu koşullara uygun, deneye ayrılmış bir dizine ayarlanmalıdır. Kontroller devre dışı bırakılmamalıdır.

```powershell
git -c core.autocrlf=false clone https://github.com/Cisco-Talos/EvidenceForge.git evidenceforge
git -C evidenceforge checkout 79fcfcdf3726168dacfede5a27aab2aa7a2f3d69
uv sync --project evidenceforge --frozen --no-dev --python 3.12
$env:PYTHONIOENCODING = 'utf-8'

& .\evidenceforge\.venv\Scripts\eforge.exe validate scenario.yaml --checkpoint-hours 0
& .\evidenceforge\.venv\Scripts\eforge.exe validate scenario-bulk.yaml --checkpoint-hours 0
& .\evidenceforge\.venv\Scripts\eforge.exe generate scenario.yaml -o run-native-a --seed 20261028 --checkpoint-hours 0
& .\evidenceforge\.venv\Scripts\eforge.exe generate scenario.yaml -o run-native-b --seed 20261028 --checkpoint-hours 0
& .\evidenceforge\.venv\Scripts\eforge.exe generate scenario-bulk.yaml -o run-bulk-a --seed 20261028 --checkpoint-hours 0
& .\evidenceforge\.venv\Scripts\eforge.exe eval run-native-a
& .\evidenceforge\.venv\Scripts\eforge.exe eval run-bulk-a
python analyze_pilot.py
```

Çıktı dizinleri yeni olmalıdır. Son komut Python standart kütüphanesiyle kayıtları ve manifest özetlerini inceleyerek `analysis_result.json` üretir. Bu yeni dosya ile kayıtlı `observed-results.json` karşılaştırılabilir. Analiz betiği üreticinin bütün kalite ölçütlerini yeniden uygulamaz; `eval` raporları ayrıca değerlendirilmelidir.

## Sonraki çalışma

Tarama hedefi amaçlanan sunucuyla eşleşecek şekilde düzeltilmeli; Suricata EVE `alert`/`flow` verisi ayrıca elde edilmelidir. Bu ön deney DSL motorunun veya AI'nin başarısını ölçmez. Beklenen sonuç etiketleri tespit girdilerinden ayrı tutulmalıdır.
