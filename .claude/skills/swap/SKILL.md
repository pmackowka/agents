---
name: swap
description: Przerabia kod w notatnikach tego kursu (Ed Donner "Master AI Agentic Engineering") z OpenAI Python SDK na natywne SDK Anthropic — ta sama logika, inny dostawca. Użyj zawsze, gdy Piotr prosi o "przerobienie"/"podmianę"/"swap" jakiegoś pliku labu (np. `1_foundations/*.pl.ipynb`, docelowo też kolejne tygodnie) na Anthropic/Claude, albo pyta czy dany notatnik już korzysta z Claude. Nie triggeruj przy ogólnych pytaniach o API Anthropic bez kontekstu konwersji pliku — do tego służy skill `claude-api`.
---

# Swap — OpenAI → Anthropic w notatnikach kursu

Piotr przerabia materiały tego kursu z OpenAI na Anthropic, plik po pliku, w miarę jak przechodzi przez kolejne laby. To nie jest zadanie jednorazowe — będzie wracał do tego skilla wielokrotnie, dla różnych plików w różnych tygodniach. Referencyjny przykład konwersji: `1_foundations/1_lab1.pl.ipynb` (przerobiony w sesji, w której powstał ten skill) — jeśli coś jest niejasne, zajrzyj tam po wzorzec.

## Zawsze najpierw: wywołaj skill `claude-api`

Zanim napiszesz jakikolwiek kod Anthropic, wywołaj skill `claude-api`, żeby dostać aktualne ID modeli, sygnaturę `messages.create()` i wzorzec inicjalizacji klienta. Ten plik celowo NIE zawiera na sztywno wpisanych ID modeli, nazw parametrów ani sygnatur metod Anthropic — Anthropic wypuszcza nowe modele i zmienia API, więc każda taka informacja zapisana tutaj prędzej czy później zacznie kłamać. Zadaniem tego skilla jest przepis konwersji i konwencje tego repo, nie zamrożona kopia dokumentacji Anthropic.

## Zakres edycji: tylko komórki kodu

Zmieniaj wyłącznie komórki kodu (importy, inicjalizację klienta, wywołania API, nazwy modeli, parsowanie odpowiedzi) — nie ruszaj komórek markdown, chyba że Piotr wyraźnie o to poprosi. Markdown w tych notatnikach tłumaczy ogólne koncepcje kursu, nie deklaruje konkretnego dostawcy, więc zostaje bez zmian.

Komentarze wewnątrz komórek kodu (linie zaczynające się od `#`) aktualizuj tam, gdzie po zmianie kodu stałyby się nieprawdziwe — np. komentarz nazywający konkretny model GPT trzeba poprawić, skoro kod poniżej wywołuje teraz model Claude. Te notatniki są dwujęzyczne: markdown jest już po polsku (to kopie `.pl.ipynb` angielskich oryginałów, zobacz `CLAUDE.md`), a komentarze w kodzie idą za ogólną konwencją repo „kod i nazwy po angielsku, komentarze po polsku” — pisz komentarze po polsku.

To samo dotyczy tekstu wewnątrz stringów wysyłanych do modelu — patrz pierwszy punkt w „Konwencje konwersji specyficzne dla tego repo” niżej (**„Tłumacz WSZYSTKIE prompty...”**). To jedna z łatwiej gubionych reguł tego skilla — sprawdź ją jawnie przy każdym pliku, nie tylko przy pierwszym przejściu.

## Konwencje konwersji specyficzne dla tego repo

- **Tłumacz WSZYSTKIE prompty do modelu na polski — zawsze, w całym pliku, niezależnie od zawężenia zakresu SDK-konwersji.** Dotyczy tekstu w `content` wiadomości (`{"role": "user", "content": "..."}`) i promptów budowanych jako zwykłe stringi/f-stringi (`question = "..."`, `message = f"""..."""`) — to ludzki tekst czytany przez model i studenta, nie składnia API, więc tłumacz go tak samo jak markdown i komentarze. Po angielsku zostaje wyłącznie faktyczna składnia kodu: nazwy zmiennych/funkcji/parametrów, klucze słowników (`"role"`, `"content"`, `"results"` itd. — cokolwiek parsowane dalej przez kod Pythona), wywołania metod SDK, nazwy modeli. Wyjątek: tekst wygenerowany dynamicznie w trakcie działania (np. `question = response.content[0].text`) nie da się przetłumaczyć z wyprzedzeniem — zostaje taki, jaki wróci z modelu. **Ta reguła NIE jest ograniczona przez zawężenie „tylko wywołania OpenAI" z labów porównawczych (lab 2 i podobne, patrz niżej)** — tamto zawężenie dotyczy wyłącznie tego, które wywołania API konwertować na Anthropic SDK, nie tego, które komórki wolno przetłumaczyć. Prompt współdzielony przez wszystkich dostawców (np. `request`/`question` zbudowane raz i wysyłane do każdego z nich, albo `judge` budujący ocenę na końcu) tłumacz zawsze, nawet jeśli żadna komórka go używająca nie jest „OpenAI-labeled”. Realny błąd z sesji referencyjnej: przy swapie `2_lab2.pl.ipynb` komórki `request` (generowanie pytania) i `judge` (prompt sędziego) zostały pominięte, bo zawężenie zakresu konwersji błędnie potraktowano jako zawężenie zakresu tłumaczenia — nie powtarzaj tego błędu.
- **Zanim napiszesz kod Anthropic — sprawdź wbudowany skill `claude-api`, nie polegaj na pamięci.** To reguła z sekcji „Zawsze najpierw: wywołaj skill `claude-api`” na górze tego pliku — powtórzona tutaj, bo to kolejna łatwa do pominięcia zasada, szczególnie w długiej sesji, gdzie początek pliku wypada z kontekstu. `claude-api` to wbudowany skill Anthropic (nie projektowy, jak `swap`), z na bieżąco aktualizowanymi ID modeli, sygnaturami `.create()`, zasadami adaptive thinking, wymogami `max_tokens` itd. Dokumentacja Anthropic zmienia się szybciej niż ten plik, więc `claude-api` jest źródłem prawdy o samym API, a `swap` — źródłem prawdy o konwencjach tego repo. Wywołuj `claude-api` na nowo dla KAŻDEGO pliku z osobna, nie tylko raz na sesję — nawet jeśli odpalałeś go wcześniej w tej samej rozmowie dla innego notatnika.
- **Styl importu 1:1 z oryginałem.** Oryginalny kod kursu robi `from openai import OpenAI` i `openai = OpenAI()` (nazwa zmiennej zasłania import klasy, nigdzie nie ma `import openai` samego modułu). Odpowiednik Anthropic ma odzwierciedlać to dokładnie: `from anthropic import Anthropic` i `anthropic = Anthropic()` — NIE `import anthropic; client = anthropic.Anthropic()`. To minimalizuje diff i zachowuje identyczną logikę pedagogiczną, o którą prosi Piotr.
- **Zmienna środowiskowa klucza:** `ANTHROPIC_API_KEY` (już rozpoznawany, opcjonalny klucz w `.env` w korzeniu repo, zgodnie z `CLAUDE.md`). Jeśli notatnik ma komórkę diagnostyczną sprawdzającą istnienie klucza (`OPENAI_API_KEY`, wypisuje prefiks) — przerób ją analogicznie na `ANTHROPIC_API_KEY`, zmieniając nazwy zmiennych (`openai_api_key` → `anthropic_api_key` itd.), zachowując ten sam wzorzec diagnostyczny przez `print`.
- **Format listy `messages`** (`[{"role": "user", "content": "..."}]`) jest strukturalnie identyczny między OpenAI a Anthropic Messages API dla ról user/assistant — zwykle komórki budujące `messages` nie wymagają zmian, tylko samo wywołanie `.create(...)` i parsowanie odpowiedzi.
- **System prompt:** OpenAI wkłada `{"role": "system", ...}` do listy `messages`. Anthropic przyjmuje `system` jako osobny parametr top-level w `.create()`, NIE w `messages`. Gdy natrafisz na notatnik budujący wiadomość systemową wewnątrz listy `messages` (pojawia się od lab 3 w górę, nie w lab 1) — wyciągnij ją do `system=`.
- **Parsowanie odpowiedzi — NIGDY nie indeksuj na sztywno `response.content[0].text`.** `response.content` to lista bloków (`ThinkingBlock`, `TextBlock`, `ToolUseBlock`...), nie gotowy tekst. Claude Opus 5 i Claude Sonnet 5 mają domyślnie włączone adaptive thinking nawet bez podania parametru `thinking` — więc `content[0]` bywa `ThinkingBlock`, a `.text` na nim rzuca `AttributeError: 'ThinkingBlock' object has no attribute 'text'`. To realny błąd, który wystąpił przy konwersji `1_lab1.pl.ipynb` (Sonnet 5) w sesji referencyjnej. Zamiast `response.content[0].text` używaj: `next(block.text for block in response.content if block.type == "text")` — dalej jednolinijkowe, dalej czytelne dla początkującego, ale odporne na kolejność/liczbę bloków. Stosuj ten wzorzec we WSZYSTKICH komórkach parsujących odpowiedź w danym notatniku, nie tylko tam, gdzie akurat wystąpił błąd — inaczej podobne komórki w tym samym pliku będą się różnić bez powodu, a model może w każdej chwili zacząć zwracać ThinkingBlock (np. przy modelu, który dziś go nie zwraca).
- **`max_tokens` jest WYMAGANY** w `.create()` Anthropic (brak wartości domyślnej) — w OpenAI jest opcjonalny. Zawsze go dodaj. NIE zaniżaj tej wartości pod pretekstem "to tylko krótka odpowiedź" — token'y zużyte na adaptive thinking (patrz punkt wyżej: domyślnie włączone na Opus 5/Sonnet 5) liczą się do tego samego limitu co widoczny tekst. Przy niskim `max_tokens` (np. 1024) model potrafi zużyć cały budżet na myślenie i nie zdążyć wygenerować żadnego bloku tekstowego — wtedy `next(block.text for block in response.content if block.type == "text")` rzuca `StopIteration`, bo generator nie znajduje niczego. To realny błąd, który wystąpił w sesji referencyjnej zaraz po naprawie błędu z `ThinkingBlock` powyżej — obie usterki mają to samo źródło. Domyślnie używaj `max_tokens=16000` (zgodnie z rekomendacją skilla `claude-api` dla zapytań non-streaming) i schodź niżej tylko z konkretnym powodem, świadomie akceptując ryzyko obcięcia.
- **Mapowanie poziomów modeli.** Laby często pokazują progresję tani/szybki → średni → flagowy w 2-3 wywołaniach (np. gpt-5.4-nano → gpt-5.4-mini → gpt-5.4 w lab 1). Zachowaj tę samą liczbę poziomów, ale konkretne ID modeli Anthropic bierz z tego, co zwróci wywołany wcześniej skill `claude-api` dla bieżącej sesji — nie zapisuj tutaj nazw typu "Haiku"/"Sonnet"/"Opus" na sztywno, bo lineup Anthropic się zmienia. Wyjątek: lab 2 (i podobne) porównuje wielu dostawców na raz obok siebie — tam NIE konwertuj wywołań oznaczonych jako OpenAI (zobacz punkt „Kod bezpośrednio wołający prawdziwe OpenAI” niżej) i nie ruszaj pozostałych dostawców (Anthropic-przez-compat, DeepSeek, Gemini, Groq, Grok, OpenRouter, Ollama) — sensem tego labu jest właśnie zestawienie wielu różnych dostawców, nie spłaszczaj tego do jednego.
- **Kod bezpośrednio wołający prawdziwe OpenAI w labach porównujących wielu dostawców (lab 2 i podobne) — zostaw go jako OpenAI, nie konwertuj na Anthropic. Ale TYLKO jeśli komórka jest liściem, nie twardą zależnością dla reszty notatnika.** Cały kurs jest domyślnie napisany pod OpenAI; Piotr świadomie nie trzyma `OPENAI_API_KEY` w `.env` repo (nie płaci za OpenAI, korzysta z Claude), więc taki kod nigdy się u niego nie uruchomi — ale to nie powód, żeby go usuwać czy zamieniać. W labach, których całym sensem jest pokazanie wielu dostawców obok siebie (np. lab 2 — `openai` jako jeden z kilku konkurentów obok `anthropic`/`deepseek`/`gemini`/...), zostaw komórkę tworzącą klienta OpenAI (`openai = OpenAI()`) i wywołania na nim w oryginalnej, angielskiej postaci OpenAI — nie dopisuj do niej żadnej wersji Anthropic. Dodaj nad taką komórką (albo na górze niej) krótki komentarz PL w stylu: `# Ten kod nie uruchomi się bez OPENAI_API_KEY w .env — celowo go nie trzymam, zostaje dla porównania z wywołaniami innych dostawców poniżej`. Nie dotyczy to labów, w których OpenAI jest jedynym albo głównym dostawcą (np. lab 1) — tam nadal obowiązuje pełna konwersja na Anthropic z reszty tego pliku, bo sensem takiego labu jest, żeby Piotr mógł faktycznie uruchomić i przerobić go na Claude.
  **Przed zostawieniem komórki jako martwego OpenAI, prześledź, czy jej wynik zasila kolejne komórki.** Rozróżnij dwa przypadki: (1) *liść* — komórka dokłada wpis do współdzielonej struktury przez wywołanie funkcji (np. `record(model_name, answer)` w lab 2), a żadna późniejsza komórka nie odwołuje się do niej po nazwie zmiennej; jeśli taka komórka nie uruchomi się, reszta notatnika i tak leci dalej (Piotr po prostu przeskakuje ją ręcznie w Jupyterze) — to bezpiecznie zostaje jako martwy OpenAI. (2) *twarda zależność* — komórka tworzy zmienną, do której odwołują się po nazwie wszystkie kolejne komórki (np. `question` w lab 2, generowane w komórce z OpenAI, zużywane w `messages = [{"role": "user", "content": question}]` i przez każdego konkurenta niżej) — taka komórka MUSI się uruchomić, więc mimo bycia „OpenAI-owym krokiem” w oryginalnym kodzie kursu, przerób ją na Anthropic tak jak w labach jedno-dostawcowych, żeby Piotr mógł w ogóle przejść dalej. Realny błąd z sesji referencyjnej: komórka generująca `question` w `2_lab2.pl.ipynb` została zostawiona jako OpenAI pod tą regułą, co zablokowało wykonanie całego reszty notatnika — poprawiona dopiero po tym, jak Piotr to zauważył przy próbie przejścia labu.

- **Pułap kosztowy: domyślnie zawsze najtańszy model — Claude Haiku 4.5.** Piotr świadomie ogranicza koszty na czas przechodzenia przez kurs — Claude Sonnet 5, Claude Opus 5 i Claude Fable 5 NIE mają się pojawiać w generowanym kodzie jako model domyślny, nawet jeśli oryginalny kod OpenAI wywoływał swój najdroższy/flagowy model (np. `gpt-5.4` bez sufiksu). Gdy notatnik pokazuje progresję tani→średni→flagowy, mapuj domyślnie WSZYSTKIE poziomy na Haiku 4.5 — jeśli spłaszczenie progresji do jednego modelu wydaje się gubić sens ćwiczenia (bo lab demonstruje właśnie różnicę jakości między warstwami), zaznacz to wprost Piotrowi zamiast cicho decydować samodzielnie. Ta zasada dotyczy warstwy modelu (którą warstwę wybrać), nie konkretnego ID — samo ID nadal bierz z `claude-api`, żeby nie zapisywać go tutaj na sztywno. Odstępstwo: użyj droższego modelu tylko wtedy, gdy Piotr wyraźnie o to poprosi (np. "użyj tu Sonnet 5" albo "użyj Opusa") — nigdy domyślnie, nawet dla górnego poziomu progresji.
- **Wywołania narzędzi (tool use, od lab 3 w górę).** OpenAI: `tools=[...]` + `response.choices[0].finish_reason == "tool_calls"` + pętla po `message.tool_calls`. Anthropic: `tools=[...]` + `response.stop_reason == "tool_use"` + iterowanie `response.content` w poszukiwaniu bloków `tool_use` + zwracanie wyników jako wiadomość `user` zawierająca bloki `tool_result` (nie wiadomość z rolą `"tool"` jak w OpenAI). To zmiana kształtu pętli, nie tylko zmiana nazw — to najbardziej pracochłonny przypadek konwersji w tym repo. Gdy się pojawi, doczytaj dokładnie dokumentację tool use w skillu `claude-api` (`shared/tool-use-concepts.md` + `{lang}/claude-api/tool-use.md`) zamiast improwizować kształt pętli z pamięci.
- **Gradio (`gr.ChatInterface(chat)`, od lab 3 w górę).** Wnętrze funkcji `chat(message, history)` się zmienia (wywołania klienta, parsowanie odpowiedzi), ale samo okablowanie Gradio jest niezależne od dostawcy i zostaje bez zmian.

## Dodawanie dodatkowego dostawcy/modelu do labów porównawczych (poza OpenAI→Anthropic)

Osobna czynność od swapu (nie dotyczy Anthropic) — laby porównawcze (lab 2 i podobne) czasem rozrastają się o kolejnego konkurenta obok istniejących, a nie o podmianę dostawcy. Ten skill jest miejscem, gdzie Piotr chce mieć taką wiedzę zebraną, bo dotyczy tych samych notatników.

### OpenRouter + model z tokenami rozumowania (reasoning)

OpenRouter udostępnia modele z widocznym rozumowaniem krok po kroku przez parametr `reasoning` w body requestu, a wynik trafia do pola `reasoning_details` w odpowiedzi. Dostęp do tego pola jest pewniejszy przez surowe `requests.post(...)` niż przez klienta `OpenAI(base_url=..., api_key=openrouter_api_key)` używanego gdzie indziej w tych notatnikach (np. cell z `moonshotai/kimi-k2.6` w lab 2) — SDK OpenAI ma typowany model odpowiedzi bez pola `reasoning_details`, więc dociąganie go bywa niepewne (`model_extra` zamiast zwykłego atrybutu). Gdy komórka istotnie korzysta z `reasoning_details`, użyj surowego `requests` zamiast klienta kompatybilnego z OpenAI i zaznacz to komentarzem PL — to świadome odstępstwo od konwencji reszty notatnika, nie przeoczenie.

Klucz: `OPENROUTER_API_KEY` (już czytany w tych notatnikach jako `openrouter_api_key`).

Wzorzec pojedynczego zapytania z włączonym reasoning (przykładowy model wybrany przez Piotra — darmowy Gemma na OpenRouter, dobre notowania w rankingach):

```python
import requests

response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    },
    json={
        "model": "google/gemma-4-26b-a4b-it:free",
        "messages": messages,
        "reasoning": {"enabled": True},
    },
)
message = response.json()["choices"][0]["message"]
answer = message["content"]
```

Kontynuacja rozmowy z zachowaniem rozumowania (multi-turn): dołóż odpowiedź asystenta do `messages` razem z `reasoning_details` bez modyfikacji — `{"role": "assistant", "content": message["content"], "reasoning_details": message.get("reasoning_details")}` — zanim wyślesz kolejne zapytanie; model kontynuuje rozumowanie od miejsca, w którym skończył. Potrzebne tylko wtedy, gdy komórka faktycznie prowadzi wieloturowy dialog z tym samym modelem — pojedyncza komórka-konkurent w stylu lab 2 (`record(model_name, answer)`) tego nie wymaga.

Streaming: dodaj `"stream": True` do body i iteruj po `response.iter_lines()` — nieistotne dla zwykłej, jednorazowej komórki-konkurenta.

## Weryfikacja po edycji

Zanim uznasz konwersję za skończoną, sprawdź, że notatnik jest nadal poprawny: ta sama liczba komórek co przed edycją, JSON się parsuje, a źródło każdej edytowanej komórki kodu przechodzi `ast.parse()` (sprawdzenie składni Pythona). Przykład takiej walidacji z sesji referencyjnej:

```python
import json, ast
nb = json.load(open('sciezka/do/pliku.pl.ipynb'))
print('cells:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        try:
            ast.parse(''.join(c['source']))
        except SyntaxError as e:
            print(f'cell idx {i}: SYNTAX ERROR: {e}')
```

Komórki-ćwiczenia z celowo niepełnym kodem (np. `response =` bez dokończenia) będą rzucać `SyntaxError` — to oczekiwane, nie traktuj tego jako błąd konwersji.

## Zakres pracy

Piotr pracuje plik po pliku, w miarę postępu przez kurs — nie zakładaj konwersji całego repo naraz. Domyślnie działaj na pliku, który Piotr nazwał w tej samej wiadomości. Pytaj o zakres tylko wtedy, gdy naprawdę jest niejednoznaczny (np. Piotr mówi "przerób następny lab" bez podania nazwy pliku).
