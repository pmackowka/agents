# Cyfrowy Bliźniak — szybki start

Wersja modułowa labu z `1_foundations/4_lab4.pl.ipynb`, spersonalizowana i przerobiona na Anthropic (Claude Haiku 4.5). Rozmawia z odwiedzającym o Twojej karierze, doświadczeniu i umiejętnościach — na bazie `linkedin.pdf` i `summary.txt` z tego folderu.

## Wymagania

- Klucz `ANTHROPIC_API_KEY` w pliku `.env` w **korzeniu repo** (nie w tym podfolderze) — `load_dotenv()` w `app.py` sam go tam znajdzie, licząc od `app.py` w górę drzewa katalogów.
- Opcjonalnie `PUSHOVER_USER` i `PUSHOVER_TOKEN` w tym samym `.env`, jeśli chcesz dostawać push na telefon, gdy ktoś zostawi kontakt albo zada pytanie bez odpowiedzi (patrz `tools.py`). Bez nich narzędzia po prostu nie wyślą powiadomienia — reszta działa normalnie.
- Zależności (`anthropic`, `gradio`, `pypdf`, `requests`, `python-dotenv`) są już w głównym `pyproject.toml` repo — nie trzeba nic osobno instalować. `requirements.txt` w tym folderze służy tylko do wdrożenia poza tym repo (np. HuggingFace Spaces, Render) i nie jest potrzebny do lokalnego uruchomienia.

## Uruchomienie

Z korzenia repo:

```bash
cd 1_foundations/twin-pm
uv run app.py
```

Otworzy się w przeglądarce pod `http://127.0.0.1:7860` (Gradio wypisze dokładny adres w terminalu).

## Personalizacja

Podmień w tym folderze:

- `linkedin.pdf` — eksport Twojego profilu LinkedIn
- `summary.txt` — krótkie podsumowanie sylwetki pierwszoosobowo

`context.py` wczytuje oba pliki i buduje z nich prompt systemowy — po zmianie plików wystarczy zrestartować `app.py`.

## Struktura

| Plik | Rola |
|---|---|
| `app.py` | klient Anthropic, pętla tool-use, uruchomienie UI Gradio |
| `context.py` | wczytuje `linkedin.pdf`/`summary.txt`, buduje `TWIN_SYSTEM_PROMPT` |
| `tools.py` | narzędzia (`record_user_details`, `record_unknown_question`) + powiadomienia Pushover |
| `styles.py` | CSS/JS/przykładowe pytania dla UI Gradio |
