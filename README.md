# Data Science Project 52 — Telco Churn Tahmin Modeli

**Modül**: DS Müfredatı — Bitirme Projesi • **Süre**: 4-6 saat

## 🎯 Proje Senaryosu

Bir telekomünikasyon şirketinde (TelcoTR) **data scientist** olarak işe başladın. Elinde **gerçek müşteri verisi** var — 7043 müşteri, 21 kolon. Yönetim diyor ki:

> "Elimizde binlerce müşterinin geçmiş verisi var ama hangi müşterinin **iptal (churn)** edeceğini bilmiyoruz. Uçtan uca bir model kur: veriyi temizle, birden fazla model dene, en iyisini seç ve bize gerçek bir performans raporu getir."

Bu senin **bitirme projen** — DS programında öğrendiğin tüm adımları tek bir uçtan uca akışta birleştireceksin:
- ✅ **Veri temizleme** (gizli boşluklar, tip dönüşümleri, eksik veri)
- ✅ **ColumnTransformer** (sayısal + kategorik kolonları ayrı işleme)
- ✅ **Pipeline** (data leakage'a karşı koruma)
- ✅ **Model karşılaştırma** (Logistic Regression vs Random Forest vs Gradient Boosting)
- ✅ **Cross-validation** (5-fold ile gerçek performans)
- ✅ **Hiperparametre optimizasyonu** (GridSearchCV)
- ✅ **Final değerlendirme** (ROC-AUC, precision, recall, f1, confusion matrix)

## 📦 Proje Kurulumu

```bash
# Fork + clone
git clone <your-fork-url>
cd data-science-project-52

# Virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate          # Windows

# Dependencies
pip install -r requirements.txt

# Auto test runner (dosya değişince çalışır)
python watch.py

# Manuel test
pytest tests/test_question.py -v
```

## 🔑 Kaizu Bağlantısı — `kaizu_config.py`

Skorunun Kaizu hesabına yazılması için **`kaizu_config.py`** dosyasını aç ve **`USER_ID`** alanını kendi user_id'nle değiştir:

```python
USER_ID = 0      # ← Kaizu profilinden alıp buraya yaz
PROJECT_ID = 0   # ← Bu projeye ait, dokunma
```

User_id'ni Kaizu profilinden bulabilirsin (Profile → Settings → User ID).

Skor göndermek için tüm testleri toplu çalıştırmalısın:

```bash
python tests/test_question.py
```

Bu komut tüm testleri çalıştırır, **passed/total oranını otomatik Kaizu'ya gönderir**. Geliştirme sırasında `pytest -v` kullanmaya devam edebilirsin (skor göndermez).

## 📊 Veri Seti

`data/telco.csv` — gerçek Telco müşteri churn verisi. 7043 müşteri, 21 kolon.

Dikkat edilecek noktalar:
- `Churn` hedefi dengesiz: **%73.5 No / %26.5 Yes**. Stratify şart.
- `TotalCharges` kolonu **string olarak gelir** ve 11 satırda gizli boşluk (`" "`) içerir — direkt sayıya çevirmeye çalışırsan hata alırsın.
- 18 kategorik kolon var → OneHotEncoder / ColumnTransformer olmadan model eğitilemez.

## 📋 Görevler (`tasks/task_manager.py`)

`task_manager.py` dosyasındaki fonksiyonları sırayla doldur. Her task altta testler pass olana kadar düzenlenmeli.

1. **`load_data(path="data/telco.csv")`** — CSV'yi pandas DataFrame olarak yükle.

2. **`explore_data(df)`** — Ham veri hakkında temel istatistikler: satır/kolon sayısı, churn oranı, kategorik/sayısal kolon sayısı.

3. **`clean_data(df)`** — `customerID` düş, `TotalCharges`'ı `pd.to_numeric(errors='coerce')` ile sayıya çevir ve oluşan NaN'leri medyanla doldur, `Churn`'ü 1/0'a çevir.

4. **`split_features_target(df)`** — Temizlenmiş veriyi `(X, y)` olarak ayır.

5. **`build_preprocessor(X)`** — `ColumnTransformer`: sayısal kolonlara `StandardScaler`, kategorik kolonlara `OneHotEncoder(handle_unknown='ignore')`.

6. **`split_data(X, y)`** — `train_test_split` ile böl. `stratify=y` ŞART (dengesiz veri), `test_size=0.2`, `random_state=42`.

7. **`train_models(preprocessor, X_train, y_train)`** — 3 model eğit, her biri `Pipeline([('prep', preprocessor), ('clf', model)])`: LogisticRegression, RandomForestClassifier, GradientBoostingClassifier.

8. **`compare_models(models, X_train, y_train, cv=5)`** — Her model için 5-fold cross-validation ROC-AUC ortalaması.

9. **`tune_best_model(preprocessor, X_train, y_train)`** — GradientBoosting üzerinde küçük bir GridSearchCV (`n_estimators`, `max_depth`).

10. **`evaluate_final(model, X_test, y_test)`** — Test setinde ROC-AUC, precision, recall, f1, confusion matrix.

## 🧪 Testler

Test dosyası: `tests/test_question.py` (15 test)

Tümü pass olmalı:
- Veri yükleme ve temel istatistikler doğru mu
- Veri temizleme (customerID yok, TotalCharges sayısal + NaN yok, Churn 0/1)
- Özellik/hedef ayrımı doğru mu
- ColumnTransformer doğru kurulmuş mu
- Stratified split çalışıyor mu
- 3 model de eğitilip predict edebiliyor mu
- Model karşılaştırma skorları makul aralıkta mı
- Hiperparametre optimizasyonu CV skoru ≥ 0.80
- Final ROC-AUC ≥ 0.82
- Data leakage guard'ı — ön işleme Pipeline içinde mi

## 📊 Beklenen Sonuçlar

```
Veri: 7043 satır, 21 kolon
Churn oranı: ~%26.5 (dengesiz)
Model karşılaştırma (CV ROC-AUC): logreg ~0.84-0.85, rf ~0.82, gb ~0.84-0.85
En iyi model (tuned): ROC-AUC ~0.84-0.85
Final test seti: ROC-AUC ≥ 0.82
```

## 💡 İpuçları

- **TotalCharges'a dikkat** — direkt `astype(float)` çağırırsan hata alırsın, önce `pd.to_numeric(errors='coerce')` kullan.
- **stratify'ı UNUTMA** — dengesiz veride yoksa test setindeki sınıf oranı kayar.
- **Pipeline kullan** — ön işlemeyi (scaler/encoder) split'ten önce tüm veriye `fit` edersen data leakage olur (fake skor). Her model için preprocessor'ı ayrı klonlaman gerekebilir.
- **CV'siz tek split şüpheli** — cross-validation ile ortalama al, tek bir random_state'e güvenme.
- **ROC-AUC dengesiz veride accuracy'den daha güvenilir** — bu yüzden tüm skorlama ROC-AUC üzerinden.

## 🎓 Öğrenme Çıktıları

Bu projeyi bitirdiğinde:
- Gerçek, kirli veriyi (string tipler, gizli boşluklar) temizlemeyi bilirsin
- ColumnTransformer ile karma (sayısal + kategorik) veriyi doğru işlemeyi bilirsin
- Birden fazla modeli adil şekilde karşılaştırmayı (CV) bilirsin
- GridSearchCV ile hiperparametre optimizasyonu yapabilirsin
- Dengesiz sınıflandırma problemlerinde doğru metrikleri (ROC-AUC, precision/recall) okuyabilirsin
- Uçtan uca bir ML projesini profesyonelce raporlayabilirsin

## 🚫 Dikkat

- `tests/test_question.py` dosyasını **değiştirme**
- `random_state=42` değerini değiştirme (testler fail olur)
- `_solution/` klasörü yok (DB'de saklanır, dersin haftası geçince açılır)
- Dokunabileceğin **2 dosya**: `tasks/task_manager.py` (kodu yaz) + `kaizu_config.py` (sadece USER_ID)
