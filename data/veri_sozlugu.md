# Veri Sözlüğü — `telco.csv`

TelcoTR müşteri kayıtları. **7043 satır** (her satır bir müşteri), **21 kolon**. Her müşterinin demografik bilgisi, aldığı hizmetler, hesap/fatura bilgisi ve son dönemde ayrılıp ayrılmadığı yer alıyor.

> Bu bir **ham** veri dosyası. Kolon tipleri ve içerikleri her zaman beklediğin gibi olmayabilir — kendi kontrolünü yapmayı unutma.

## Kolonlar

| Kolon | Açıklama | Beklenen değerler |
|---|---|---|
| `customerID` | Müşteri kimlik numarası (her satır benzersiz) | ör. `7590-VHVEG` |
| `gender` | Cinsiyet | `Female`, `Male` |
| `SeniorCitizen` | Müşteri 65+ mı | `0` (hayır), `1` (evet) |
| `Partner` | Eşi/partneri var mı | `Yes`, `No` |
| `Dependents` | Bakmakla yükümlü olduğu kişi var mı | `Yes`, `No` |
| `tenure` | TelcoTR'de kaç aydır müşteri | tam sayı, 0–72 |
| `PhoneService` | Telefon hizmeti alıyor mu | `Yes`, `No` |
| `MultipleLines` | Birden fazla hattı var mı | `Yes`, `No`, `No phone service` |
| `InternetService` | İnternet hizmeti türü | `DSL`, `Fiber optic`, `No` |
| `OnlineSecurity` | Online güvenlik ek hizmeti | `Yes`, `No`, `No internet service` |
| `OnlineBackup` | Online yedekleme ek hizmeti | `Yes`, `No`, `No internet service` |
| `DeviceProtection` | Cihaz koruma ek hizmeti | `Yes`, `No`, `No internet service` |
| `TechSupport` | Teknik destek ek hizmeti | `Yes`, `No`, `No internet service` |
| `StreamingTV` | TV yayın hizmeti | `Yes`, `No`, `No internet service` |
| `StreamingMovies` | Film yayın hizmeti | `Yes`, `No`, `No internet service` |
| `Contract` | Sözleşme türü | `Month-to-month`, `One year`, `Two year` |
| `PaperlessBilling` | Kağıtsız (dijital) fatura | `Yes`, `No` |
| `PaymentMethod` | Ödeme yöntemi | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` |
| `MonthlyCharges` | Aylık ücret | ondalık sayı, ~18–119 |
| `TotalCharges` | Toplam ödenmiş tutar | müşteri başına toplam (dikkatli incele) |
| `Churn` | **Hedef değişken** — müşteri ayrıldı mı | `Yes`, `No` |

## Notlar

- **Hedef değişken** `Churn`. Amacın bunu tahmin etmek.
- `tenure = 0` olan müşteriler çok yeni (henüz bir tam ay dolmamış) kayıtlardır.
- `No internet service` / `No phone service` değerleri "bilgi eksik" değildir — müşterinin o ana hizmeti almadığını gösterir; anlamlı bir bilgidir.
