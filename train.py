"""
train.py
--------
TelcoTR müşteri kaybı (churn) tahmin modeli - final, tek komutla çalışan training akışı.

Bu script, analiz.ipynb'de keşfedilen kararların (veri temizliği, ön işleme, model seçimi) sadeleştirilmiş,
notebook anlatımından arındırılmış hâlidir. Amaç: 'python train.py' çalıştırıldığında veriyi okuyup
final modeli (Random Forest) eğitip sonuç metriklerini ekrana basmak.

Kullanımı:
    python train.py
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score, average_precision_score, classification_report, confusion_matrix,
)

RANDOM_STATE = 42
DATA_PATH = "data/telco.csv"

# Numeric / categorical column listeleri notebook'taki keşfe dayanıyor.
NUMERIC_COLS = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen"]
# Categorical column'lar veri okunduktan sonra geri kalan object column'lardan otomatik türetiliyor.

def load_and_clean_data(path: str) -> pd.DataFrame:
    """
    CSV'yi okur ve analiz.ipynb'de tespit edilen bilinen veri kalitesi sorunlarını düzeltir.
    
    Düzeltilen sorunlar:
    - TotalCharges kolonu 'object' tipinde geliyor; 11 satırda tek boşluk (' ') karakteri var. Bunların hepsi tenure=0 olan
    yani henüz 1. ayını doldurmamış yeni müşteriler. Sayıya çevirip 0 ile dolduruyorum.
    - customerID modelden çıkarılıyor. Benzersiz bir kimlik, öngörü gücü yok.
    """
    
    df = pd.read_csv(path)
    
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(0)
    
    df = df.drop(columns=["customerID"])
    
    return df


def split_features_and_target(df: pd.DataFrame):
    """
    Hedef değişkeni (Churn) 0/1'e çevirir ve X/y olarak ayırır.
    """
    
    X = df.drop(columns=["Churn"])
    y = (df["Churn"] == "Yes").astype(int)
    
    return X, y


def build_pipeline(categorical_cols: list) -> Pipeline:
    """
    Ön işleme ve model adımlarını tek bir Pipeline'da birleştirir.
    
    Pipeline kullanmamın sebebi: train_test_split sonrası çağırılan .fit() sadece X_train üzerinde
    istatistik (ölçekleme için ortalama/standart sapma, one-hot kategorileri) öğrenir; X_test'e sadece
    .transform() uygulanır. Bu, data leakage'ı yapısal olarak engeller.
    """
    
    preprocess = ColumnTransformer([
        ("num", StandardScaler(), NUMERIC_COLS),
        ("cat", OneHotEncoder(handle_unknown="ignore", drop="first"), categorical_cols)
    ])
    
    """
    Final model: Random Forest. Gerekçe (bkz. analiz.ipynb bölüm 9): Lojistik Regresyon ile aynı recall'u,
    daha az false positive ile sağlıyor. Bu, daha iyi precision ve aynı erken uyarı gücü anlamına geliyor.
    class_weight="balanced": hedef dengesiz (%73,5 / %26,5); azınlık sınıfına (Churn="Yes") daha fazla
    ağırlık vererek modelin yalnızca çoğunluk sınıfını tahmin etmesini engelliyor.
    """
    
    model = RandomForestClassifier(
        n_estimators=400,
        max_depth=8,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    
    return Pipeline([
        ("prep", preprocess),
        ("model", model)
    ])
    

def main():
    df = load_and_clean_data(DATA_PATH)
    X, y = split_features_and_target(df)
    categorical_cols = [c for c in X.columns if c not in NUMERIC_COLS]
    
    # stratify=y: hedef dengesiz olduğu için train/test setlerinde aynı churn oranını koruyorum.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=RANDOM_STATE
    )
    
    pipe = build_pipeline(categorical_cols)
    pipe.fit(X_train, y_train)
    
    y_pred = pipe.predict(X_test)
    y_prob = pipe.predict_proba(X_test)[:, 1]
    
    naive_accuracy = (y_test == 0).mean()
    
    print("=" * 60)
    print("TelcoTR Churn Modeli - Final Sonuçlar (Random Forest)")
    
    print("=" * 60)
    print(f"Train size: {X_train.shape} | Test size: {X_test.shape}")
    print(f"Test setindeki gerçek Churn oranı: {y_test.mean():.4f}")
    print(f"Naif 'herkes kalır' tahmininin accuracy değeri: {naive_accuracy:.4f} <- referans taban çizgi")
    
    print("=" * 60)
    print(f"ROC-AUC : {roc_auc_score(y_test, y_prob):.4f}")
    print(f"PR-AUC : {average_precision_score(y_test, y_prob):.4f}")
    
    print("=" * 60)
    print(classification_report(y_test, y_pred, digits=3, target_names=["Kalır (No)", "Ayrılır (Yes)"]))
    print("Confusion Matrix [[TN FP] [FN TP]]:")
    print(confusion_matrix(y_test, y_pred))
    
    print("=" * 60)

if __name__ == "__main__":
    main()