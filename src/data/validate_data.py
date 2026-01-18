import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw" / "dane.csv"

df = pd.read_csv(DATA_PATH)

print("Liczba wierszy:", len(df))
print("\nKolumny:")
print(df.columns)

print("\nPrzykładowe dane:")
print(df.head())

print("\nRozkład satisfied:")
print(df["satisfied"].value_counts())