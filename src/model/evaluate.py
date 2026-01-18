import pandas as pd
from pathlib import Path
import joblib

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

#ŚCIEŻKI
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "dane.csv"
MODEL_PATH = BASE_DIR / "models" / "model.pkl"

#WCZYTANIE DANYCH
df = pd.read_csv(DATA_PATH)

X = df.drop("satisfied", axis=1)
y = df["satisfied"]

#WCZYTANIE MODELU
pipeline = joblib.load(MODEL_PATH)

#PREDYKCJA
y_pred = pipeline.predict(X)

#METRYKI
print("=== CLASSIFICATION REPORT ===")
print(classification_report(y, y_pred))

#CONFUSION MATRIX
cm = confusion_matrix(y, y_pred)
disp = ConfusionMatrixDisplay(cm)
disp.plot(cmap="Blues")
plt.title("Confusion Matrix – Full Dataset")
plt.show()
