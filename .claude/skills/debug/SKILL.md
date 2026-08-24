---
name: debug
description: Debuguje błędy w kodzie tego kursu (notatniki, skrypty) bez konieczności ponownego odpalania Jupytera od zera — izoluje zawodzące wywołanie API i konstruuje minimalną, samodzielną reprodukcję (zwykle curl), którą Piotr odpala sam przez `!` w tej samej rozmowie, bo Bash ma zablokowany bezpośredni odczyt `.env`. Triggeruj, gdy Piotr wkleja traceback/błąd z uruchomionej komórki albo prosi o pomoc w debugowaniu — nie czekaj na jawne wywołanie, wklejony błąd wystarczy.
---

# Debug — debugowanie kodu w tym repo bez przeładowywania notatnika

Piotr pracuje w Jupyterze (Cursor/VS Code, kernel `.venv`). Odpalenie notatnika od nowa po zmianie jednej komórki oznacza przejście wszystkich poprzedzających kroków, żeby odtworzyć zmienne (`messages`, `question`, klientów providerów itd.) — kosztowne czasowo. Ten skill istnieje, żeby debugować pojedynczą zawodzącą komórkę/wywołanie API bez tego przeładowania, izolując je do samodzielnej reprodukcji poza Jupyterem.

## Twardy constraint: Bash nie czyta `.env`

W tym środowisku Bash ma zablokowany (permission deny) bezpośredni dostęp do `.env` w korzeniu repo — potwierdzone empirycznie w sesji referencyjnej (`cat`/`grep`/`test -f .env` w Bashu = odmowa). Nie próbuj tego obchodzić żadnym pośrednim sposobem (skrypt Pythona ładujący `.env` przez `load_dotenv()` i odpalany przez Bash prawdopodobnie trafi w tę samą blokadę albo złamie intencję zabezpieczenia) — to świadoma granica, nie usterka do obejścia. Jedyna droga do faktycznego klucza: poproś Piotra, żeby sam odpalił polecenie przez `!` na początku wiadomości (patrz sesja-specyficzna instrukcja w systemowym prompcie) — `!` uruchamia komendę w JEGO sesji, więc `.env` jest czytany lokalnie, a output (bez samego klucza) wraca do rozmowy.

## Workflow

1. **Zbierz błąd.** Traceback wklejony przez Piotra, albo — jeśli wskazał plik — przeczytaj zawodzącą komórkę (Read/NotebookEdit).
2. **Zidentyfikuj dokładne wywołanie, które zawiodło:** dostawca, endpoint/`base_url`, model, nazwa zmiennej env z kluczem, payload (messages, parametry).
3. **Zbuduj minimalną, samodzielną reprodukcję — domyślnie curl.** Nie wymaga `uv`/stanu Pythona z notatnika, nagłówki proste, nie zależy od zmiennych zdefiniowanych w innych komórkach:
   ```
   ! set -a && source .env && set +a && curl -s <endpoint> -H "Authorization: Bearer $<NAZWA_KLUCZA>" -H "Content-Type: application/json" -d '<minimalny JSON payload, np. jedna wiadomość "Hello">'
   ```
   Dla dostawców OpenAI-compatible w notatnikach tygodnia 1 (`ANTHROPIC_BASE_URL`, `DEEPSEEK_BASE_URL`, `GEMINI_BASE_URL`, `GROQ_BASE_URL`, `GROK_BASE_URL`, `OPENROUTER_BASE_URL`, `OLLAMA_BASE_URL` — zdefiniowane w `1_foundations/2_lab2.pl.ipynb` i analogicznych) użyj dokładnie tego samego `base_url` i modelu co w zawodzącej komórce.
4. **Poproś Piotra o wklejenie tego z prefiksem `!`** w tej samej rozmowie (nie osobny terminal) — output wyląduje jako `<bash-stdout>`/`<bash-stderr>` w kolejnej wiadomości.
5. **Diagnozuj na podstawie FAKTYCZNEJ treści odpowiedzi** (kod HTTP, pole `error`), nie zgaduj przyczyny z samego tracebacku Pythona. Wyjątki w Pythonie (`KeyError`, `AttributeError`) często maskują prawdziwy powód — provider zwraca błąd jako HTTP 200 z ciałem `{"error": {...}}`, więc surowe indeksowanie (`response.json()["choices"]`) rzuca mylący `KeyError` zamiast czytelnego komunikatu.
6. **Popraw właściwą komórkę (NotebookEdit) dopiero po potwierdzeniu przyczyny.** Nie "naprawiaj" kodu spekulacyjnie bez zobaczenia realnej treści błędu — to prowadzi do fixów, które nie adresują faktycznej przyczyny (np. zmiana modelu, gdy problem to przeciążony rate limit).
7. **Zwaliduj jak przy `swap`:** ta sama liczba komórek co przed edycją, edytowana komórka przechodzi `ast.parse()`.

## Częste przyczyny w tym repo (sprawdź, zanim zaczniesz zgadywać)

- **Brak klucza dla danego dostawcy.** Notatniki tygodnia 1 mają komórkę diagnostyczną (wzorzec z `2_lab2.pl.ipynb`, cell z `openai_api_key = os.getenv(...)` + `if/else print`) — sprawdź ją najpierw, zanim zaczniesz debugować samo wywołanie API.
- **Surowe `requests` do endpointu OpenAI-compatible/OpenRouter: błąd przychodzi jako HTTP 200 z `{"error": {...}}`, NIE jako wyjątek.** Zawsze sprawdź `"choices" in response.json()` przed indeksowaniem — inaczej dostajesz nieczytelny `KeyError: 'choices'` zamiast realnego powodu.
- **Modele `:free` na OpenRouterze dzielą wspólną, przeciążalną pulę u dostawcy pod spodem** (np. Google AI Studio dla Gemma). `HTTP 429 "temporarily rate-limited upstream"` jest częste i przejściowe, NIE błąd kodu — dodaj retry z kilkusekundowym sleep (2-3 próby), nie zmieniaj modelu ani klucza w reakcji na to.
- **Natywny Anthropic SDK:** `AttributeError: 'ThinkingBlock' object has no attribute 'text'` i `StopIteration` przy parsowaniu `response.content` — to już opisane w skillu `swap` (sztywne indeksowanie `response.content[0].text` / za niski `max_tokens`). Nie duplikuj tej wiedzy tutaj, tylko odeślij do `swap`.
- **Zanim zaproponujesz fix dotyczący samego Anthropic API** (nazwa parametru, ID modelu, sygnatura metody) — wywołaj skill `claude-api`, tak jak w `swap`. Nie zgaduj z pamięci.

## Realny przykład z sesji referencyjnej

`google/gemma-4-26b-a4b-it:free` przez OpenRouter (`2_lab2.pl.ipynb`) rzucał `KeyError: 'choices'`. Zamiast zgadywać (zła nazwa modelu? zły klucz?), zweryfikowano model przez WebSearch (poprawny, istnieje na OpenRouterze), potem Piotr odpalił `! set -a && source .env && set +a && curl ...` z dokładnie tym samym payloadem co w komórce. Odpowiedź: `HTTP 429`, `"google/gemma-4-26b-a4b-it:free is temporarily rate-limited upstream"` — współdzielona darmowa pula, nie bug. Fix: retry z sleep + walidacja `"choices" in response.json()` przed indeksowaniem, żeby przyszły podobny błąd był czytelny od razu, bez tej całej procedury.

## Zakres

To repo ma wiele pod-projektów (notatniki tygodnia 1, CrewAI tydzień 3, Sidekick tydzień 4, Mastra/TS tydzień 5, trading floor tydzień 6/6_mcp) — sama technika (izoluj najmniejszą zawodzącą jednostkę, unikaj re-run całości, respektuj blokadę `.env`, poproś Piotra o `!`) generalizuje się poza notatniki tygodnia 1, ale konkretne przykłady (curl, `base_url`) dotyczą głównie multi-provider notebooków, bo tam Piotr najczęściej trafia na tego typu błędy.
