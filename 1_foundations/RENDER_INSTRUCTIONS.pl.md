# Wdrożenie cyfrowego bliźniaka na Render

_Jeśli czytasz to w Cursorze, kliknij prawym przyciskiem na plik w eksploratorze plików i wybierz "Open Preview", żeby zobaczyć sformatowaną wersję_

HuggingFace Spaces wymaga teraz płatnej subskrypcji PRO do hostowania aplikacji Gradio, więc oto alternatywa: [Render](https://render.com). Render ma darmowy plan, nie wymaga karty kredytowej i uruchomi cyfrowego bliźniaka dokładnie w takiej postaci, w jakiej jest, bez zmian w kodzie.

Jedna rzecz do wiedzenia z góry: na darmowym planie aplikacja usypia po 15 minutach bez odwiedzających. Kolejny odwiedzający ją budzi, co zajmuje 30-60 sekund. Potem działa normalnie.

## Czego potrzebujesz

- Konto GitHub (prawdopodobnie już je masz, skoro sklonowałeś repo tego kursu)
- Twój klucz API Anthropic oraz user i token Pushover z pliku `.env`
- Katalog `twin-pm`, zaktualizowany o Twój własny `linkedin.pdf` i `summary.txt`

## Krok 1: Wydziel bliźniaka do osobnego repozytorium GitHub

Render wdraża z repozytorium GitHub. To repo kursu do tego nie nada się, bo zawiera też wszystko inne i należy do kursu. Potrzebujesz małego, osobnego repo zawierającego wyłącznie zawartość katalogu `twin-pm`.

Najprostszy sposób, bez żadnych komend gita:

1. Wejdź na [github.com/new](https://github.com/new) i utwórz repozytorium. Nazwij je `twin-pm`. Wybierz **Private**, bo Twój PDF z LinkedIn jest danymi osobowymi. Zaznacz opcję dodania README, żeby repo nie było puste.
2. Na stronie nowego repo kliknij **Add file**, potem **Upload files**.
3. Przeciągnij te 7 plików z `1_foundations/twin-pm` na swoim komputerze: `app.py`, `context.py`, `tools.py`, `styles.py`, `requirements.txt`, `summary.txt` i `linkedin.pdf`. Nie dołączaj folderu `__pycache__`, jeśli go widzisz.
4. Kliknij **Commit changes**.

Jeśli wolisz linię poleceń: najpierw skopiuj folder `twin-pm` gdzieś poza to repo kursu (na przykład `cp -r twin-pm ~/twin-pm`), potem odpal `git init`, zacommituj pliki i wypchnij do nowego prywatnego repo GitHub w zwykły sposób. Kopiowanie ma znaczenie, bo tworzenie repo gita wewnątrz repo kursu powoduje zamieszanie.

Nigdy nie wrzucaj pliku `.env` ani żadnych kluczy API do repo. Twoje klucze trafią do panelu Render w Kroku 4.

## Krok 2: Załóż konto Render

1. Wejdź na [render.com](https://render.com) i kliknij **Sign In**, potem zarejestruj się kontem GitHub. To ułatwia kolejny krok.
2. Zweryfikuj e-mail, jeśli o to poprosi. Nie musisz podawać karty kredytowej.

## Krok 3: Utwórz web service

1. W panelu Render kliknij **New +** i wybierz **Web Service**.
2. Połącz konto GitHub, jeśli o to poprosi, i daj Renderowi dostęp do repozytorium `twin-pm`.
3. Wybierz repozytorium `twin-pm`.
4. Wypełnij ustawienia:
   - **Language**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free
5. Jeszcze nie klikaj Deploy. Najpierw dodaj zmienne środowiskowe poniżej.

## Krok 4: Zmienne środowiskowe

W sekcji **Environment Variables** na tej samej stronie (albo później w zakładce **Environment** serwisu) dodaj te pięć:

| Key | Value |
|---|---|
| `ANTHROPIC_API_KEY` | Twój klucz Anthropic z `.env` |
| `PUSHOVER_USER` | Twój user Pushover z `.env` |
| `PUSHOVER_TOKEN` | Twój token Pushover z `.env` |
| `GRADIO_SERVER_NAME` | `0.0.0.0` |
| `GRADIO_SERVER_PORT` | `10000` |

Dwie ostatnie wymagają słowa wyjaśnienia. Render oczekuje, że aplikacja będzie nasłuchiwać ruchu webowego na porcie 10000, a Gradio odczytuje te dwie zmienne przy starcie — w ten sposób mówimy Gradio, gdzie ma nasłuchiwać. Żadnych zmian w kodzie.

## Krok 5: Wdróż

1. Kliknij **Deploy Web Service**.
2. Obserwuj logi. Pierwszy build trwa kilka minut, w trakcie instalacji zależności.
3. Gdy w logach zobaczysz komunikat startowy Gradio, aplikacja działa. URL jest na górze strony i wygląda jak `https://twin-pm-xxxx.onrender.com`.
4. Otwórz go i przywitaj się z bliźniakiem. Sprawdź, czy przychodzi powiadomienie Pushover, gdy podasz mu swój adres e-mail.

## Aktualizacja bliźniaka

Gdy zmienisz plik (na przykład poprawisz `summary.txt`), wgraj nową wersję do repo GitHub albo zrób push, jeśli używasz linii poleceń. Render zauważa zmianę i wdraża ją automatycznie ponownie.

## Rozwiązywanie problemów

- **Strona ładuje się bardzo długo.** Jeśli nikt nie odwiedził aplikacji od 15 minut, jest uśpiona i budzi się nawet minutę. To normalne na darmowym planie.
- **Build się nie udaje.** Sprawdź logi na stronie serwisu. Najczęstsza przyczyna to brakujący plik — upewnij się, że wszystkie 7 plików jest w repo GitHub.
- **Aplikacja się buduje, ale strona pokazuje błąd.** Zwykle brakująca albo błędnie wpisana zmienna środowiskowa. Sprawdź wszystkie pięć w zakładce **Environment**, potem użyj **Manual Deploy**, żeby zrestartować.
- **Brak powiadomień Pushover.** Sprawdź `PUSHOVER_USER` i `PUSHOVER_TOKEN` w zakładce Environment i pamiętaj, że klucz usera zaczyna się na `u`, a token na `a`.
