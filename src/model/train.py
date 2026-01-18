import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score
)

#ŚCIEŻKI
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "dane.csv"
MODEL_PATH = BASE_DIR / "models" / "model.pkl"

#WCZYTANIE DANYCH
df = pd.read_csv(DATA_PATH)

X = df.drop("satisfied", axis=1)
y = df["satisfied"]

#PODZIAŁ NA TRAIN / TEST
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#KOLUMNY
categorical_cols = [
    "preferred_activity",
    "budget",
    "travel_type",
    "season",
    "location_preference",
    "location_type",
    "cost_level",
    "main_activity"
]

numerical_cols = ["family_friendly"]

#PREPROCESSING
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", "passthrough", numerical_cols)
    ]
)

#INTERAKCJE CECH
poly = PolynomialFeatures(
    degree=2,
    interaction_only=True,
    include_bias=False
)

#MODEL (MOCNA REGULARYZACJA)
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    C=0.05,          
)

#PIPELINE
pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("poly", poly),
        ("model", model)
    ]
)

#TRENING
pipeline.fit(X_train, y_train)

#FEATURE IMPORTANCE
ohe = pipeline.named_steps["preprocessor"].named_transformers_["cat"]
feature_names_ohe = list(ohe.get_feature_names_out(categorical_cols)) + numerical_cols
poly_feature_names = poly.get_feature_names_out(feature_names_ohe)

coefs = pipeline.named_steps["model"].coef_[0]
feature_importance = (
    pd.DataFrame({"feature": poly_feature_names, "coef": coefs})
    .sort_values(by="coef", ascending=False)
)

print("\nTOP 10 CECH:")
print(feature_importance.head(10))

#EWALUACJA: TEST
y_test_pred = pipeline.predict(X_test)

print("\n=== CLASSIFICATION REPORT (TEST) ===")
print(classification_report(y_test, y_test_pred))

cm = confusion_matrix(y_test, y_test_pred)
ConfusionMatrixDisplay(cm).plot()
plt.title("Confusion Matrix – Test")
plt.show()

#OVERFITTING CHECK
y_train_pred = pipeline.predict(X_train)

train_f1 = f1_score(y_train, y_train_pred)
test_f1 = f1_score(y_test, y_test_pred)

print(f"\nF1 TRAIN (class 1): {train_f1:.3f}")
print(f"F1 TEST  (class 1): {test_f1:.3f}")
print(f"DIFFERENCE: {abs(train_f1 - test_f1):.3f}")

#CROSS-VALIDATION
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_scores = cross_val_score(
    pipeline,
    X,
    y,
    cv=cv,
    scoring="f1"
)

print("\n=== CROSS-VALIDATION (F1) ===")
print("Scores:", cv_scores)
print(f"Mean F1: {cv_scores.mean():.3f}")
print(f"Std  F1: {cv_scores.std():.3f}")

#ZAPIS MODELU
joblib.dump(pipeline, MODEL_PATH)
print(f"\nModel zapisany w: {MODEL_PATH}")
