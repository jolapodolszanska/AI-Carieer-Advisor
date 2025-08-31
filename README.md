# AI Career Advisor (PL)

**AI Career Advisor** to prosty doradca zawodowy w języku polskim oparty o **spaCy** i **Gradio**. Aplikacja dopasowuje zawody do zainteresowań użytkownika, porównując podobieństwo semantyczne pomiędzy wpisanym opisem zainteresowań a krótkimi opisami zawodów (z wykorzystaniem wektorów językowych spaCy). Interfejs webowy (Gradio) prezentuje wyniki w formie estetycznych kart z paskami postępu i tabeli Top-K.

---

## Spis treści
- [Opis](#opis)
- [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
- [Użycie](#użycie)
- [Edycja listy zawodów](#edycja-listy-zawodów)
- [Rozwiązywanie problemów (FAQ)](#rozwiązywanie-problemów-faq)
- [Architektura i decyzje](#architektura-i-decyzje)
- [Struktura projektu (propozycja)](#struktura-projektu-propozycja)
- [Licencja](#licencja)

---

## Opis
Projekt to pojedynczy skrypt – np. `app_gradio_career_advisor.py` – uruchamiany lokalnie. Po wpisaniu zainteresowań (np. „analiza danych, Python, statystyka") aplikacja oblicza podobieństwo semantyczne względem opisów zawodów i pokazuje najlepiej dopasowane propozycje.

Wykorzystujemy **polski model spaCy**:
- Zalecany: `pl_core_news_md` (zawiera wektory → lepsze dopasowania).
- Fallback: `pl_core_news_sm` (działa, ale podobieństwo może być słabsze).

**Wymagania**: Python 3.9+ (Windows/macOS/Linux) oraz dostęp do internetu przy pierwszym pobraniu modelu spaCy. Rekomendowane jest wirtualne środowisko `venv`.

---

## Instalacja i uruchomienie

Poniżej **jeden** skondensowany blok zawierający wszystko: Windows, macOS/Linux, alternatywę z `requirements.txt` oraz start aplikacji.

```bash
# =========================================
# WINDOWS (PowerShell)
# =========================================
# 1) Utwórz i aktywuj środowisko
py -m venv .venv
. .venv\Scripts\Activate.ps1

# 2) Zainstaluj paczki
py -m pip install -U pip
py -m pip install -U spacy gradio pandas

# 3) Pobierz polski model spaCy (zalecany md)
py -m spacy download pl_core_news_md

# 4) Uruchom aplikację
py app_gradio_career_advisor.py


# =========================================
# macOS / LINUX (bash/zsh)
# =========================================
# 1) Utwórz i aktywuj środowisko
python3 -m venv .venv
source .venv/bin/activate

# 2) Zainstaluj paczki
python3 -m pip install -U pip
python3 -m pip install -U spacy gradio pandas

# 3) Pobierz polski model spaCy (zalecany md)
python3 -m spacy download pl_core_news_md

# 4) Uruchom aplikację
python3 app_gradio_career_advisor.py


# =========================================
# ALTERNATYWA: requirements.txt (oba systemy)
# =========================================
# Utwórz plik requirements.txt z treścią:
#   spacy
#   gradio
#   pandas
# Następnie w aktywnym środowisku:
pip install -r requirements.txt
python -m spacy download pl_core_news_md
# Start:
python app_gradio_career_advisor.py     # albo na Windows: py app_gradio_career_advisor.py
```

Po starcie w konsoli pojawi się adres, np. `http://127.0.0.1:7860`. Otwórz go w przeglądarce.

## Użycie

1. Wpisz swoje zainteresowania (np. „analiza danych, statystyka, Python").
2. Ustaw liczbę propozycji (Top-K).
3. Kliknij „Znajdź zawód" lub naciśnij Enter.
4. Odczytaj tabelę i karty z procentowym dopasowaniem oraz krótkim opisem zawodów.

## Edycja listy zawodów

W skrypcie znajduje się lista `CAREERS` (zawód + opis). Dodaj nowe pozycje, np.:

```python
CAREERS = [
    {"Zawód": "Nowy zawód", "Opis": "Słowa kluczowe, kompetencje, kontekst pracy..."},
    # ...
]
```

Im trafniej opiszesz kompetencje i słowa kluczowe, tym lepsze będą dopasowania.

## Rozwiązywanie problemów (FAQ)

### Błąd: `OSError: [E050] Can't find model 'pl_core_news_md'`

Model nie jest zainstalowany w aktywnym interpreterze. Zainstaluj go w tym samym środowisku, z którego uruchamiasz aplikację:

```bash
# Windows
py -m spacy download pl_core_news_md
# macOS / Linux
python3 -m spacy download pl_core_news_md
```

Weryfikacja zgodności wersji spaCy i modeli:

```bash
python -m spacy validate
```

Sprawdzenie, którego Pythona używasz (czy instalujesz do właściwego środowiska):

```bash
python -c "import sys; print(sys.executable)"
```

### Inne typowe przyczyny:

- Model zainstalowany w innym środowisku / innym interpreterze (sprawdź, jaki interpreter ustawiłeś w VS Code/PyCharm).
- Brak uprawnień/sieci przy instalacji modelu.
- Zbyt stary Python (użyj 3.9+).

## Architektura i decyzje

- **NLP**: spaCy + `pl_core_news_md` → `Doc.similarity()` do porównania semantycznego zainteresowań z opisami zawodów.
- **UI**: Gradio Blocks – lekki, lokalny i responsywny interfejs webowy.
- **Dane**: wbudowana lista zawodów w kodzie; łatwo przenieść do CSV/JSON i ładować przez pandas.
- **Jakość dopasowania**: używaj modelu `md` (posiada wektory); `sm` to awaryjny fallback z gorszym podobieństwem.

## Struktura projektu (propozycja)

```
.
├─ app_gradio_career_advisor.py   # główny skrypt
├─ requirements.txt               # opcjonalne: zależności
└─ README.md                      # ten plik
```

## Licencja

Dodaj wybraną licencję (np. MIT / Apache-2.0).
