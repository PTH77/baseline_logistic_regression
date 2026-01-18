# Projekt danych – Agent Turystyczny (ML)

## 1. Cel etykiety `satisfied`

Etykieta `satisfied` przyjmuje wartość 1, jeżeli dana oferta turystyczna
jest zgodna z preferencjami użytkownika w stopniu pozwalającym uznać ją
za satysfakcjonującą. W przeciwnym wypadku przyjmuje wartość 0.

Celem modelu nie jest idealna predykcja satysfakcji, lecz identyfikacja
przypadków, w których istnieje wysokie prawdopodobieństwo zadowolenia
użytkownika.

---

## 2. Założenia projektowe

1. Satysfakcja użytkownika nie jest losowa – wynika z dopasowania cech oferty.
2. Nie wszystkie cechy mają jednakową wagę decyzyjną.
3. Model może popełniać false positives, jeżeli zwiększa to recall klasy 1.
4. Dane są syntetyczne, ale projektowane w sposób logiczny i interpretowalny.

---

## 3. Reguły przypisywania satysfakcji (GROUND TRUTH)

Satysfakcja (`satisfied = 1`) jest przypisywana, gdy spełnione są
co najmniej **2 z 3 głównych warunków**:

### 3.1 Główne warunki

- preferred_activity == main_activity
- location_preference == location_type
- budget == cost_level

### 3.2 Warunki wspierające (bonus)

- Jeżeli travel_type == "family" oraz family_friendly == True,
  zwiększa to prawdopodobieństwo satysfakcji.

- Jeżeli season jest zgodny z location_type (np. summer + beach),
  traktowane jest to jako czynnik pozytywny, lecz niewystarczający samodzielnie.

---

## 4. Przykładowe przypadki decyzyjne

### Przypadek 1 – SATISFIED = 1

preferred_activity: sightseeing  
main_activity: sightseeing  
location_preference: city  
location_type: city  
budget: medium  
cost_level: medium  
travel_type: couple  
family_friendly: False  

Uzasadnienie:
Spełnione są 3 główne warunki. Oferta jest w pełni dopasowana do preferencji.

---

### Przypadek 2 – SATISFIED = 1

preferred_activity: relax  
main_activity: relax  
location_preference: beach  
location_type: beach  
budget: low  
cost_level: medium  
travel_type: family  
family_friendly: True  

Uzasadnienie:
Spełnione są 2 główne warunki oraz warunek bonusowy (rodzina).

---

### Przypadek 3 – SATISFIED = 0

preferred_activity: active  
main_activity: sightseeing  
location_preference: mountains  
location_type: city  
budget: low  
cost_level: high  
travel_type: solo  
family_friendly: False  

Uzasadnienie:
Brak zgodności kluczowych cech, wysoki koszt i brak czynników wspierających.
