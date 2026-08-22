# Wdrażanie swojego bliźniaka na Render

_Jeśli oglądasz to w Cursorze, kliknij prawym przyciskiem na plik w File Explorerze i wybierz "Open Preview", żeby zobaczyć sformatowaną wersję_

HuggingFace Spaces wymaga teraz płatnej subskrypcji PRO, żeby hostować aplikacje Gradio, więc oto alternatywa: [Render](https://render.com). Render ma darmowy plan, nie wymaga karty kredytowej i może uruchomić bliźniaka dokładnie takim, jaki jest, bez zmian w kodzie.

Jedna rzecz, o której warto wiedzieć z góry: na darmowym planie Twoja aplikacja usypia po 15 minutach bez odwiedzających. Kolejny odwiedzający budzi ją, co zajmuje 30 do 60 sekund. Potem odpowiada normalnie.

## Czego będziesz potrzebować

- Konta GitHub (prawdopodobnie już je masz z klonowania tego kursu)
- Swojego klucza API OpenAI oraz swojego usera i tokena Pushover, z pliku `.env`
- Katalogu `twin`, zaktualizowanego o Twój własny `linkedin.pdf` i `summary.txt`

## Krok 1: Umieść bliźniaka we własnym repozytorium GitHub

Render wdraża z repozytorium GitHub. To repozytorium kursu do tego się nie nada, bo zawiera też wszystko inne i należy do kursu. Chcesz małe, osobne repozytorium, zawierające tylko zawartość katalogu `twin`.

Najłatwiejszy sposób, całkowicie bez poleceń git:

1. Wejdź na [github.com/new](https://github.com/new) i utwórz repozytorium. Nazwij je `twin`. Wybierz **Private**, bo Twój PDF z LinkedIn jest prywatny. Zaznacz opcję dodania README, żeby repozytorium nie było puste.
2. Na stronie swojego nowego repo kliknij **Add file**, a potem **Upload files**.
3. Przeciągnij tych 7 plików z `1_foundations/twin` na swoim komputerze: `app.py`, `context.py`, `tools.py`, `styles.py`, `requirements.txt`, `summary.txt` i `linkedin.pdf`. Nie dołączaj folderu `__pycache__`, jeśli go widzisz.
4. Kliknij **Commit changes**.

Jeśli wolisz linię poleceń: najpierw skopiuj folder `twin` gdzieś poza to repozytorium kursu (np. `cp -r twin ~/twin`), a potem uruchom `git init`, zacommituj pliki i wypchnij do nowego prywatnego repozytorium GitHub w zwykły sposób. Kopiowanie ma znaczenie, bo tworzenie repozytorium git wewnątrz repozytorium kursu powoduje zamieszanie.

Nigdy nie umieszczaj swojego pliku `.env` ani żadnych kluczy API w repozytorium. Twoje klucze trafią do panelu Render w Kroku 4.

## Krok 2: Utwórz konto Render

1. Wejdź na [render.com](https://render.com) i kliknij **Sign In**, a potem zarejestruj się przez swoje konto GitHub. To ułatwia następny krok.
2. Zweryfikuj swój email, jeśli zostaniesz o to poproszony. Nie musisz podawać karty kredytowej.

## Krok 3: Utwórz web service

1. Z panelu Render kliknij **New +** i wybierz **Web Service**.
2. Połącz swoje konto GitHub, jeśli zostaniesz o to poproszony, i daj Render dostęp do swojego repozytorium `twin`.
3. Wybierz repozytorium `twin`.
4. Wypełnij ustawienia:
   - **Language**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free
5. Jeszcze nie klikaj Deploy. Najpierw dodaj zmienne środowiskowe poniżej.

## Krok 4: Zmienne środowiskowe

W sekcji **Environment Variables** na tej samej stronie (albo później pod zakładką **Environment** usługi) dodaj tych pięć:

| Klucz | Wartość |
|---|---|
| `OPENAI_API_KEY` | Twój klucz OpenAI z `.env` |
| `PUSHOVER_USER` | Twój user Pushover z `.env` |
| `PUSHOVER_TOKEN` | Twój token Pushover z `.env` |
| `GRADIO_SERVER_NAME` | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | `10000` |

Ostatnie dwie wymagają słowa wyjaśnienia. Render oczekuje, że Twoja aplikacja będzie nasłuchiwać ruchu webowego na porcie 10000, a Gradio odczytuje te dwie zmienne przy starcie, więc w ten sposób mówimy Gradio, gdzie ma nasłuchiwać. Żadnych zmian w kodzie nie potrzeba.

## Krok 5: Wdróż

1. Kliknij **Deploy Web Service**.
2. Obserwuj logi. Pierwszy build zajmuje kilka minut, gdy instaluje wymagania.
3. Gdy zobaczysz w logach komunikat startowy Gradio, Twoja aplikacja działa. URL jest na górze strony i wygląda jak `https://twin-xxxx.onrender.com`.
4. Otwórz go i przywitaj się ze swoim bliźniakiem. Sprawdź, czy przychodzi powiadomienie Pushover, gdy podasz mu swój adres email.

## Aktualizowanie swojego bliźniaka

Gdy zmienisz plik (np. poprawisz `summary.txt`), wyślij nową wersję do repozytorium GitHub, albo zrób push, jeśli używałeś linii poleceń. Render zauważa zmianę i wdraża ponownie automatycznie.

## Rozwiązywanie problemów

- **Strona ładuje się wieki.** Jeśli nikt nie odwiedził przez 15 minut, aplikacja śpi i budzi się do minuty. To normalne na darmowym planie.
- **Build się nie udaje.** Sprawdź logi na stronie usługi. Najczęstszą przyczyną jest brakujący plik, więc potwierdź, że wszystkie 7 plików jest w repozytorium GitHub.
- **Aplikacja się buduje, ale strona pokazuje błąd.** Zazwyczaj brakująca albo źle wpisana zmienna środowiskowa. Sprawdź wszystkie pięć w zakładce **Environment**, a potem użyj **Manual Deploy**, żeby zrestartować.
- **Brak powiadomień Pushover.** Sprawdź `PUSHOVER_USER` i `PUSHOVER_TOKEN` w zakładce Environment i pamiętaj, że klucz usera zaczyna się od `u`, a token od `a`.
