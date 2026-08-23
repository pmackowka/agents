---
name: solve
description: Dopisuje przykładowe, działające rozwiązanie ćwiczenia (komórka markdown "Ćwiczenie"/"Exercise" + zwykle niepełny szkic kodu pod nią) w notatnikach tego kursu (Ed Donner "Master AI Agentic Engineering"), np. `1_foundations/*.pl.ipynb`. Użyj zawsze, gdy Piotr prosi o "zrobienie"/"rozwiązanie"/"uzupełnienie" ćwiczenia w konkretnym pliku labu, o dopisanie przykładowej odpowiedzi pod ćwiczeniem, albo pyta czy dany plik ma już rozwiązanie zadania. Nie triggeruj przy podmianie dostawcy API (OpenAI→Anthropic) — do tego służy skill `swap`, choć oba często idą w parze (najpierw swap całego pliku, potem solve dla ćwiczenia w nim).
---

# Solve — przykładowe rozwiązania ćwiczeń w labach

Każdy lab w tym kursie kończy się komórką "Ćwiczenie"/"Exercise" (markdown, zwykle w kolorowej tabelce) i zaraz pod nią szkicem kodu do samodzielnego dokończenia przez studenta — często celowo niepełnym (np. `response =` bez dokończenia linii). Piotr czasem prosi o dopisanie własnego, działającego rozwiązania obok tego szkicu, żeby mieć punkt odniesienia albo zobaczyć jak to mogłoby wyglądać.

## Zanim napiszesz kod: wywołaj skill `claude-api`

Ta sama zasada co w `swap` — nigdy nie zgaduj z pamięci ID modeli, sygnatury `messages.create()` ani parametrów. Wywołaj skill `claude-api` po aktualne dane, zanim zaczniesz pisać wywołania API.

## Nie ruszaj istniejącego szkicu ćwiczenia

Komórka ze szkicem (ta niepełna, tuż pod treścią ćwiczenia) jest tam celowo — to szablon do samodzielnej próby, nie coś do naprawienia. Twoje rozwiązanie dopisz w NOWYCH komórkach WSTAWIONYCH ZARAZ PO tym szkicu, nie w miejscu szkicu i nie zamiast niego. Przed swoim kodem wstaw krótką komórkę markdown, np.:

```
### Przykładowe rozwiązanie (niezależne od szkicu powyżej)

<jedno zdanie streszczające kroki, np. "Łańcuch 3 wywołań LLM: obszar biznesowy → bolączka → propozycja rozwiązania.">
```

Dzięki temu Twoje rozwiązanie jest wyraźnie odróżnione od miejsca, gdzie student ma próbować sam.

## Przeczytaj treść ćwiczenia dosłownie

Treść komórki "Ćwiczenie" mówi dokładnie, ile wywołań LLM potrzeba i jak mają się ze sobą łączyć (zwykle wynik jednego wywołania trafia do promptu następnego — łańcuch, nie niezależne zapytania). Odtwórz dokładnie tę liczbę kroków i tę kolejność, nie dodawaj dodatkowych "usprawnień" ani nie upraszczaj do mniejszej liczby wywołań, niż opisano.

## Konwencje kodu w tym repo (spójne ze skillem `swap`)

- Klient: zmienna `anthropic` (`from anthropic import Anthropic` + `anthropic = Anthropic()`), zgodnie z resztą pliku — sprawdź, czy notatnik już go zainicjował wcześniej (prawie zawsze tak, skoro to plik po `swap`); jeśli tak, użyj tej samej instancji zamiast tworzyć nową.
- **Pułap kosztowy: domyślnie `model="claude-sonnet-5"`.** Piotr świadomie ogranicza koszty na czas przechodzenia przez kurs — nie sięgaj po Claude Opus 5 ani Claude Fable 5, chyba że wyraźnie o to poprosi albo zadanie realnie wymaga zdolności poza warstwą Sonnet (rzadkie na tym etapie kursu). Pełne uzasadnienie tej zasady: `.claude/skills/swap/SKILL.md`.
- `max_tokens=16000` — nie zaniżaj tej wartości. Adaptive thinking (domyślnie włączone na modelach Claude 5) liczy się do tego samego limitu co widoczny tekst; zbyt niska wartość (np. 1024) potrafi uciąć odpowiedź, zanim model napisze cokolwiek tekstowego — realny błąd (`StopIteration`) napotkany w sesji referencyjnej.
- Parsowanie odpowiedzi: `next(block.text for block in response.content if block.type == "text")` — NIGDY `response.content[0].text` (pierwszy blok bywa `ThinkingBlock`, nie tekstem — drugi realny błąd napotkany w sesji referencyjnej).
- Komentarze w kodzie i treść promptów przekazywanych do modelu piszesz po polsku (ten notatnik jest już po polsku w całości — markdown, komentarze i prompty). Nazwy zmiennych, funkcji, kluczy słowników i wywołania API zostają w oryginalnej, angielskiej składni.
- Do wyświetlenia finalnego wyniku użyj `display(Markdown(...))`, jeśli `from IPython.display import Markdown, display` już wystąpiło wcześniej w notatniku (prawie zawsze tak) — nie importuj ponownie, po prostu użyj.

## Wstawianie kilku nowych komórek NotebookEdit — sposób bez zgadywania ID

Tryb `insert` w NotebookEdit nie zwraca w wyniku ID nowo utworzonej komórki, więc żeby wstawić drugą komórkę zaraz po pierwszej, trzeba by odczytać cały plik między jednym insertem a drugim. Szybszy sposób: wstawiaj wszystkie nowe komórki w KOLEJNOŚCI ODWROTNEJ, za każdym razem z tym samym `cell_id` oryginalnej komórki-kotwicy (czyli szkicu ćwiczenia albo Twojej komórki markdown-nagłówka). Każdy insert ląduje bezpośrednio po tej samej kotwicy, spychając poprzedni insert niżej — więc wstawiając np. 3 komórki w kolejności [KROK 3, KROK 2, KROK 1], finalny układ na dysku wychodzi poprawny: KROK 1, KROK 2, KROK 3. Oszczędza to odczyt pliku między każdym insertem.

Jedyny moment, w którym i tak trzeba odczytać plik, to koniec pracy — weryfikacja (patrz niżej).

## Weryfikacja po dodaniu komórek

Nie masz sposobu, żeby faktycznie wykonać komórki notatnika (nie masz uruchomionego kernela Jupyter) — nie udawaj, że sprawdziłeś realny output, i powiedz to wprost Piotrowi na końcu. Możesz i powinieneś sprawdzić za to statycznie:

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

Oczekiwany wyjątek: sam oryginalny szkic ćwiczenia (celowo niepełny) będzie dalej rzucał `SyntaxError` — to nie błąd Twojej pracy, zostaw go bez zmian. Każdy inny `SyntaxError` to prawdziwy problem do naprawienia.

Na koniec powiedz Piotrowi, żeby uruchomił notatnik od nowo dodanych komórek w dół w Cursorze i sprawdził wynik — to jedyny sposób na realną weryfikację, że łańcuch wywołań działa.

## Zakres pracy

Działaj na pliku, który Piotr nazwał w tej samej wiadomości. Jeśli w danym pliku jest więcej niż jedno ćwiczenie (rzadkie, ale możliwe w dłuższych labach), albo nie jest jasne, o które ćwiczenie chodzi, zapytaj zamiast zgadywać.
