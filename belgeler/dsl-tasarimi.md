# DSL tasarım taslağı

Dil, güvenlik olayları üzerinde sınırlı ve doğrulanabilir tespit ifadeleri sunacaktır. Kesin gramer ve operatör öncelikleri uygulama sırasında sürümlenecektir.

## Örnek

```text
rule ssh_failures {
    source linux_auth;
    detect count(linux_auth.auth_failure) >= 5;
    in 60s;
    by src_ip;
    then alert "Repeated SSH login failures";
}
```

Bu [tasarım örneği](../ornekler/ssh_basarisiz_girisler.dsl), aynı kaynak IP'den 60 saniyede en az beş ayrı SSH kimlik doğrulama başarısızlığı için alarmı ifade eder. Eşik ve süre, senaryo üzerinde değerlendirilecek başlangıç değerleridir. Henüz bu dosyayı çalıştıran bir güvenlik DSL ayrıştırıcısı yayımlanmamıştır.

## Kural türleri

| Tür | Senaryo | Motor sorumluluğu |
|---|---|---|
| Alan koşulu | Belirli IP/ağ, protokol ve port koşulu | Tür denetimli karşılaştırma ve mantıksal koşullar |
| Olay sayımı | Aynı IP'den 60 saniyede en az 5 SSH başarısızlığı | Grup/pencere sayacı |
| Benzersiz değer sayımı | Aynı kaynak/hedef için 20 farklı hedef portu | Flow kayıtlarında tekrar portları bir kez sayma |
| Sırasız çok kaynaklı ilişki | Ağ uyarısı ile SSH başarısızlıklarının aynı pencerede görülmesi | Aynı grup içinde iki koşulun birlikte sağlanması |
| İki aşamalı sıralı ilişki | Başarısızlık eşiğinden sonra başarılı giriş | Grup eşleştirme, sıralama ve zaman aşımı |

İstisnalar ilgili kuralın açık koşullarıdır. Örneğin yetkili tarayıcı IP'si yalnızca ilgili tarama kuralından hariç tutulabilir.

## Şablonlar ve doğrulama

Hazır şablonlar kopyalanıp özelleştirilebilir; kullanıcı desteklenen DSL ile kendi şablonunu kaydedebilir. Parametreli şablondan üretilen kural da normal doğrulama ve test hattından geçer. Şablon değişikliği etkin kuralı kendiliğinden değiştirmez.

Lark sözdizimini işler. AST (Abstract Syntax Tree: soyut sözdizim ağacı) anlamsal denetimden sonra IR'ye (Intermediate Representation: ara gösterim) dönüştürülür. Bilinmeyen kaynak/alan, geçersiz eşik/süre ve desteklenmeyen gruplama reddedilir. Zaman penceresi ve olay sayımı tespit motorunda uygulanır.
