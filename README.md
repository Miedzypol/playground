# Epo Playground

> **CLI do komunikacji z Agentami AI**

Epo Playground to narzędzie wiersza poleceń do interakcji z modelami AI, inspirowane interfejsami Pi oraz OpenCode CLI. Obecnie korzysta z API OpenRouter, z planami migracji na własny serwer w przyszłości.

---

## ✨ Funkcje

- **Interaktywny interfejs CLI** – Czytelny, kolorowy interfejs z obsługą komend
- **Wiele modeli AI** – Obsługa różnych modeli z OpenRouter
- **Modele lokalne** – Możliwość uruchamiania lokalnych modeli GGUF poprzez llama-cpp-python
- **Strumieniowanie odpowiedzi** – Odpowiedzi wyświetlane w czasie rzeczywistym
- **Zarządzanie sesjami** – Rozpoczynanie nowych sesji i czyszczenie historii
- **System prompty** – Konfigurowalne prompty systemowe dla różnych modeli
- **Pobieranie modeli** – Wbudowany system pobierania modeli lokalnych
- **Autouzupełnianie** – Inteligentne podpowiadanie komend

---

## 📦 Instalacja

### Wymagania
- Python 3.10 lub nowszy
- pip (menedżer pakietów Python)

### Szybka instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/Miedzypol/playground.git
cd playground

# Utwórz wirtualne środowisko (opcjonalnie, ale zalecane)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate  # Windows

# Zainstaluj zależności
pip install -r requirements.txt

# Skopiuj plik konfiguracyjny środowiska
cp .env.example .env

# Edytuj .env i dodaj swój klucz API OpenRouter
nano .env  # Linux/Mac
# lub
notepad .env  # Windows
```

---

## ⚙️ Konfiguracja

### Klucz API OpenRouter

1. Zarejestruj się na [OpenRouter](https://openrouter.ai/)
2. Wygeneruj klucz API w panelu użytkownika
3. Dodaj klucz do pliku `.env`:

```env
OPENROUTER_API_KEY=twoj_klucz_api_tutaj
```

### Opcjonalne ustawienia

W pliku `.env` możesz również zdefiniować domyślny model:

```env
MODEL=mistralai/mistral-nemo
```

---

## 🚀 Użycie

### Uruchomienie

```bash
python app.py
```

### Dostępne komendy

| Komenda | Opis |
|---------|------|
| `/help` | Wyświetla pomoc |
| `/clear` | Czyści ekran |
| `/exit` | Zamknięcie aplikacji |
| `/new` | Rozpoczyna nową sesję (czyści historię czatu) |
| `/model` | Zmiana modelu AI |
| `/menu` | Otwiera menu aplikacji |

### Podstawowa interakcja

Po uruchomieniu możesz od razu zadawać pytania:

```
>> Cześć, jak się masz?

AI: Cześć! Mam się dobrze, dziękuję za pytanie. Jak mogę Ci pomóc?

>> /model
# Otwiera interaktywny wybór modelu

>> /new
Started new session.

>> /exit
Bye!
```

---

## 🔧 Modele lokalne

### Obsługiwane modele

Aplikacja obsługuje lokalne modele w formacie GGUF, uruchamiane poprzez `llama-cpp-python`.

### Dostępne serie modeli

- **Mosaic v1** – Model QuickFix-2B

### Pobieranie modeli

1. Wybierz opcję "Przetestuj lokalnie modele Epo..." z menu
2. Wybierz serię modeli (np. Mosaic v1)
3. Aplikacja automatycznie pobierze model i system prompt (jeśli dostępny)

Modele są przechowywane w katalogu `models/` w strukturze:
```
models/
└── mosaic/
    └── v1/
        ├── mosaic-v1-quickfix.gguf
        └── system-prompt.md
```

### Ręczne dodawanie modeli

1. Umieść plik `.gguf` w katalogu `models/<seria>/<wersja>/`
2. Opcjonalnie: dodaj plik `system-prompt.md` w tym samym katalogu
3. Uruchom aplikację – modele zostaną automatycznie wykryte

---

## 📁 Struktura projektu

```
playground/
├── app.py              # Główna aplikacja CLI
├── utils.py            # Funkcje narzędziowe
├── config.ini          # Konfiguracja aplikacji
├── requirements.txt    # Zależności Python
├── .env.example        # Szablon zmiennych środowiskowych
├── .gitignore          # Ignorowane pliki
├── LICENSE             # Licencja (BSD 3-Clause)
└── AGENTS.md           # Wytyczne dla agentów AI
```

---

## 📝 Konfiguracja

### config.ini

```ini
[General]
version = 1.2
default_model = mistralai/mistral-nemo
```

### Dostępne modele (domyślne)

- `recursive/flint-v1.0:free`
- `poolside/laguna-s-2.1:free`
- `mistralai/mistral-nemo` (domyślny)
- `inclusionai/ling-3.0-flash`
- `openai/gpt-oss-120b`

---

## 🔄 Migracja na własny serwer

W przyszłości planowana jest migracja z OpenRouter API na własny serwer do komunikacji z modelami AI. Struktura aplikacji jest przygotowana na tę zmianę.

---

## 🤝 Wkład

Wkłady są mile widziane! Jeśli chcesz pomóc:

1. Rozpocznij fork repozytorium
2. Utwórz nowy branch (`git checkout -b feature/nazwa`)
3. Dokonaj zmian i commit (`git commit -m 'Dodano nową funkcję'`)
4. Wyślij Pull Request

---

## 📄 Licencja

Projekt jest udostępniany na licencji **BSD 3-Clause License**.

Szczegóły w pliku [LICENSE](LICENSE).

---

## 🏢 Autor

**Project Aurly** (a̳yllo)

---

## 📞 Kontakt

W przypadku pytań lub problemów, otwórz Issue w repozytorium GitHub.

---

*Epo Playground v1.2 | © 2026 Project Aurly*
