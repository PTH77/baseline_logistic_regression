import random
import csv
from pathlib import Path

#ŚCIEŻKI
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_PATH = BASE_DIR / "data" / "raw" / "dane.csv"

#WARTOŚCI
activities = ["relax", "sightseeing", "active"]
location_types = ["city", "mountains", "beach"]
budgets = ["low", "medium", "high"]
travel_types = ["solo", "couple", "family"]
seasons = ["summer", "winter", "fall", "spring"]

#LOGIKA SUKCESU
def is_satisfied(user, location):
    score = 0

    if user["preferred_activity"] == location["main_activity"]:
        score += 2

    if user["budget"] == location["cost_level"]:
        score += 1

    if user["travel_type"] == "family" and location["family_friendly"]:
        score += 2

    if user["location_preference"] == location["location_type"]:
        score += 2

    if user["season"] == "summer" and location["location_type"] == "beach":
        score += 1

    return 1 if score >= 4 else 0

#GENEROWANIE DANYCH
rows = []

for _ in range(500):
    user = {
        "preferred_activity": random.choice(activities),
        "budget": random.choice(budgets),
        "travel_type": random.choice(travel_types),
        "season": random.choice(seasons),
        "location_preference": random.choice(location_types + ["none"])
    }

    location = {
        "location_type": random.choice(location_types),
        "cost_level": random.choice(budgets),
        "main_activity": random.choice(activities),
        "family_friendly": random.choice([True, False])
    }

    satisfied = is_satisfied(user, location)

    rows.append([
        user["preferred_activity"],
        user["budget"],
        user["travel_type"],
        user["season"],
        user["location_preference"],
        location["location_type"],
        location["cost_level"],
        location["main_activity"],
        location["family_friendly"],
        satisfied
    ])

#ZAPIS DO CSV
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "preferred_activity",
        "budget",
        "travel_type",
        "season",
        "location_preference",
        "location_type",
        "cost_level",
        "main_activity",
        "family_friendly",
        "satisfied"
    ])
    writer.writerows(rows)
