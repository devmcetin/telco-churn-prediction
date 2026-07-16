"""
DS-52 — Telco Churn Tahmin Modeli
Gerçek bir telekom şirketinin müşteri verisiyle uçtan uca bir churn (kayıp)
tahmin modeli kuruyorsun: veri temizleme, ön işleme, model karşılaştırma,
hiperparametre optimizasyonu ve final değerlendirme.

Her fonksiyonun NotImplementedError satırını sil, kendi kodunu yaz. Testleri
çalıştır, hepsi geçene kadar iterate et: `python watch.py` veya
`pytest tests/test_question.py -v`
"""


# 1. Veriyi yükle
def load_data(path="data/telco.csv"):
    """
    CSV dosyasını pandas DataFrame olarak yükle.

    Args:
        path: CSV dosya yolu (default "data/telco.csv")

    Returns:
        pandas.DataFrame
    """
    raise NotImplementedError("load_data henüz yazılmadı")


# 2. Veriyi keşfet
def explore_data(df):
    """
    Ham veri hakkında temel istatistikleri çıkar.

    Args:
        df: ham DataFrame (henüz temizlenmemiş)

    Returns:
        dict: {
            'n_rows': int,
            'n_cols': int,
            'churn_rate': float (Churn == 'Yes' oranı),
            'n_categorical': int (kategorik/metin kolon sayısı),
            'n_numeric': int (sayısal kolon sayısı),
        }

    İpucu: df.select_dtypes(include=...) ile kolonları dtype'a göre ayırabilirsin.
    """
    raise NotImplementedError("explore_data henüz yazılmadı")


# 3. Veriyi temizle
def clean_data(df):
    """
    Veriyi modele hazır hale getir:
    - `customerID` kolonunu düş (model için anlamsız).
    - `TotalCharges` string olarak gelir, 11 satırda gizli boşluk (" ") var.
      `pd.to_numeric(..., errors='coerce')` ile sayıya çevir, oluşan NaN'leri
      medyanla doldur.
    - `Churn` kolonunu 1/0'a çevir (Yes=1, No=0).

    Args:
        df: ham DataFrame

    Returns:
        pandas.DataFrame (temizlenmiş)
    """
    raise NotImplementedError("clean_data henüz yazılmadı")


# 4. Özellik / hedef ayrımı
def split_features_target(df):
    """
    Temizlenmiş DataFrame'i özellik matrisi (X) ve hedef vektöre (y) ayır.

    Args:
        df: temizlenmiş DataFrame (clean_data çıktısı)

    Returns:
        tuple: (X pandas.DataFrame, y pandas.Series) — Churn X'te olmamalı.
    """
    raise NotImplementedError("split_features_target henüz yazılmadı")


# 5. Ön işleme pipeline'ı
def build_preprocessor(X):
    """
    Sayısal ve kategorik kolonlara ayrı işlem uygulayan bir ColumnTransformer kur:
    - Sayısal kolonlar → StandardScaler
    - Kategorik kolonlar → OneHotEncoder(handle_unknown='ignore')

    Args:
        X: özellik DataFrame'i (split_features_target çıktısı)

    Returns:
        sklearn.compose.ColumnTransformer

    İpucu: X.select_dtypes(...) ile sayısal/kategorik kolon isimlerini ayır.
    """
    raise NotImplementedError("build_preprocessor henüz yazılmadı")


# 6. Train/test split
def split_data(X, y):
    """
    train_test_split kullan:
    - test_size=0.2
    - stratify=y (dengesiz veri — sınıf oranı korunmalı)
    - random_state=42

    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    raise NotImplementedError("split_data henüz yazılmadı")


# 7. Modelleri eğit
def train_models(preprocessor, X_train, y_train):
    """
    3 farklı model eğit, her biri Pipeline([('prep', preprocessor), ('clf', model)])
    şeklinde kurulmalı (data leakage'a karşı koruma):
    - LogisticRegression(max_iter=1000)
    - RandomForestClassifier(random_state=42)
    - GradientBoostingClassifier(random_state=42)

    Args:
        preprocessor: build_preprocessor çıktısı
        X_train, y_train: eğitim verisi

    Returns:
        dict: {'logreg': fitted Pipeline, 'rf': fitted Pipeline, 'gb': fitted Pipeline}

    İpucu: preprocessor'ı her pipeline için ayrı ayrı klonlamalısın
    (sklearn.base.clone) — aksi halde aynı nesneyi paylaşırlar.
    """
    raise NotImplementedError("train_models henüz yazılmadı")


# 8. Modelleri karşılaştır (CV)
def compare_models(models, X_train, y_train, cv=5):
    """
    Her model için cv-fold cross_val_score (scoring='roc_auc') ortalamasını hesapla.

    Args:
        models: train_models çıktısı (dict of fitted Pipeline)
        X_train, y_train: eğitim verisi
        cv: fold sayısı (default 5)

    Returns:
        dict: {'logreg': mean_auc, 'rf': mean_auc, 'gb': mean_auc} (float değerler)
    """
    raise NotImplementedError("compare_models henüz yazılmadı")


# 9. En iyi modeli hiperparametre ile ayarla
def tune_best_model(preprocessor, X_train, y_train):
    """
    GradientBoostingClassifier üzerinde küçük bir GridSearchCV yap:
    - param_grid: clf__n_estimators=[50, 100], clf__max_depth=[2, 3]
    - scoring='roc_auc', cv=3

    Args:
        preprocessor: build_preprocessor çıktısı
        X_train, y_train: eğitim verisi

    Returns:
        dict: {
            'best_estimator': en iyi fitted Pipeline,
            'best_params': dict,
            'best_score': float,
        }
    """
    raise NotImplementedError("tune_best_model henüz yazılmadı")


# 10. Final değerlendirme
def evaluate_final(model, X_test, y_test):
    """
    Test setinde final metrikleri hesapla.

    Args:
        model: eğitilmiş en iyi Pipeline (predict_proba destekliyor olmalı)
        X_test, y_test: test verisi

    Returns:
        dict: {
            'roc_auc': float (predict_proba ile),
            'precision': float,
            'recall': float,
            'f1': float,
            'confusion_matrix': [[tn, fp], [fn, tp]],
        }
    """
    raise NotImplementedError("evaluate_final henüz yazılmadı")


if __name__ == "__main__":
    df = load_data()
    print("📊 Keşif:", explore_data(df))

    df = clean_data(df)
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)

    models = train_models(preprocessor, X_train, y_train)
    comparison = compare_models(models, X_train, y_train)
    print("📊 Model karşılaştırma (CV ROC-AUC):", comparison)

    tuned = tune_best_model(preprocessor, X_train, y_train)
    print("📊 En iyi parametreler:", tuned["best_params"], "CV skoru:", tuned["best_score"])

    final = evaluate_final(tuned["best_estimator"], X_test, y_test)
    print("📊 Test sonuçları:", final)
