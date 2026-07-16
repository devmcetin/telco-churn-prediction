import pytest
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tasks.task_manager import (
    load_data,
    explore_data,
    clean_data,
    split_features_target,
    build_preprocessor,
    split_data,
    train_models,
    compare_models,
    tune_best_model,
    evaluate_final,
)


# 1. load_data
def test_load_data_shape():
    df = load_data()
    assert df.shape == (7043, 21)


# 2. explore_data
def test_explore_data_format():
    df = load_data()
    info = explore_data(df)
    assert isinstance(info, dict)
    assert set(info.keys()) == {
        "n_rows",
        "n_cols",
        "churn_rate",
        "n_categorical",
        "n_numeric",
    }
    assert info["n_rows"] == 7043
    assert info["n_cols"] == 21


def test_explore_data_churn_rate_and_dtypes():
    df = load_data()
    info = explore_data(df)
    assert abs(info["churn_rate"] - 0.265) < 0.01
    assert info["n_categorical"] == 18
    assert info["n_numeric"] == 3


# 3. clean_data
def test_clean_data_drops_customer_id():
    df = load_data()
    cleaned = clean_data(df)
    assert "customerID" not in cleaned.columns


def test_clean_data_total_charges_numeric():
    df = load_data()
    cleaned = clean_data(df)
    assert pd_is_numeric(cleaned["TotalCharges"])
    assert cleaned["TotalCharges"].isna().sum() == 0


def test_clean_data_churn_binary():
    df = load_data()
    cleaned = clean_data(df)
    assert set(cleaned["Churn"].unique()) == {0, 1}
    assert str(cleaned["Churn"].dtype) in ("int64", "int32")


def pd_is_numeric(series):
    import pandas as pd

    return pd.api.types.is_numeric_dtype(series)


# 4. split_features_target
def test_split_features_target():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    assert "Churn" not in X.columns
    assert set(y.unique()) == {0, 1}
    assert len(X) == len(y)


# 5. build_preprocessor
def test_build_preprocessor_structure():
    from sklearn.compose import ColumnTransformer

    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    assert isinstance(preprocessor, ColumnTransformer)
    transformed = preprocessor.fit_transform(X)
    assert transformed.shape[0] == X.shape[0]


# 6. split_data
def test_split_data_sizes():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    assert len(X_train) + len(X_test) == len(X)
    assert abs(len(X_test) / len(X) - 0.2) < 0.01


def test_split_data_stratified_ratio():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = split_data(X, y)
    train_ratio = y_train.mean()
    test_ratio = y_test.mean()
    assert abs(train_ratio - test_ratio) < 0.03


# 7. train_models
def test_train_models_returns_pipelines():
    from sklearn.pipeline import Pipeline

    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    models = train_models(preprocessor, X_train, y_train)
    assert set(models.keys()) == {"logreg", "rf", "gb"}
    for pipe in models.values():
        assert isinstance(pipe, Pipeline)
        preds = pipe.predict(X_test[:5])
        assert len(preds) == 5


# 8. compare_models
def test_compare_models_scores():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    models = train_models(preprocessor, X_train, y_train)
    scores = compare_models(models, X_train, y_train, cv=5)
    assert set(scores.keys()) == {"logreg", "rf", "gb"}
    for score in scores.values():
        assert isinstance(score, float)
        assert 0.5 <= score <= 1.0


# 9. tune_best_model
def test_tune_best_model():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    result = tune_best_model(preprocessor, X_train, y_train)
    assert set(result.keys()) == {"best_estimator", "best_params", "best_score"}
    assert result["best_score"] >= 0.80
    preds = result["best_estimator"].predict(X_test[:5])
    assert len(preds) == 5


# 10. evaluate_final
def test_evaluate_final_metrics():
    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    tuned = tune_best_model(preprocessor, X_train, y_train)
    result = evaluate_final(tuned["best_estimator"], X_test, y_test)
    assert set(result.keys()) == {
        "roc_auc",
        "precision",
        "recall",
        "f1",
        "confusion_matrix",
    }
    assert result["roc_auc"] >= 0.82
    for key in ("precision", "recall", "f1"):
        assert 0.0 <= result[key] <= 1.0
    cm = result["confusion_matrix"]
    assert len(cm) == 2 and len(cm[0]) == 2 and len(cm[1]) == 2


# 11. Data leakage guard — scaler Pipeline içinde olmalı (fit sadece train'de)
def test_no_data_leakage_preprocessor_inside_pipeline():
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer

    df = clean_data(load_data())
    X, y = split_features_target(df)
    preprocessor = build_preprocessor(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    models = train_models(preprocessor, X_train, y_train)
    for pipe in models.values():
        assert isinstance(pipe, Pipeline)
        assert isinstance(pipe.named_steps["prep"], ColumnTransformer)
        # preprocessor Pipeline'ın ilk adımı olmalı, ayrı fit edilip
        # X_train + X_test birlikte transform edilmemeli
        assert pipe.steps[0][0] == "prep"


# ──────────────────────────────────────────────────────
# Kaizu skor gönderimi — bu kısma DOKUNMA
# ──────────────────────────────────────────────────────

import requests


def _send_score(user_score):
    """Kaizu API'sine skor gönder. user_id ve project_id kaizu_config'ten gelir."""
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from kaizu_config import USER_ID, PROJECT_ID
    except ImportError:
        print("⚠️  kaizu_config.py bulunamadı — skor gönderilmeyecek.")
        return

    if USER_ID == 0:
        print("⚠️  kaizu_config.py'de USER_ID=0 — kendi ID'ni yazmadın, skor gönderilmeyecek.")
        return

    url = "https://kaizu-api-8cd10af40cb3.herokuapp.com/projectLog"
    payload = {
        "user_id": USER_ID,
        "project_id": PROJECT_ID,
        "user_score": user_score,
        "is_auto": True,
    }
    try:
        r = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if r.status_code in (200, 201):
            print(f"✅ Skor gönderildi: {user_score}")
        else:
            print(f"⚠️  Skor gönderilemedi (HTTP {r.status_code})")
    except Exception as e:
        print(f"⚠️  Skor gönderilirken hata: {e}")


class _ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1


def run_tests():
    """Tüm testleri çalıştır + skoru Kaizu'ya gönder."""
    collector = _ResultCollector()
    pytest.main([os.path.dirname(__file__), "-q"], plugins=[collector])
    total = collector.passed + collector.failed
    if total == 0:
        print("Hiç test çalışmadı.")
        return
    user_score = round((collector.passed / total) * 100, 2)
    print(f"\n📊 Toplam başarılı : {collector.passed}/{total}")
    print(f"📊 Skor            : {user_score}")
    _send_score(user_score)


if __name__ == "__main__":
    run_tests()
