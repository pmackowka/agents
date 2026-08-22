# Notebooki w Cursorze

Ten kurs intensywnie wykorzystuje wspaniałą rzecz zwaną Notebookami (znanymi też jako Jupyter Notebooks albo Labs). Osoby z tradycyjnym backgroundem inżynierii oprogramowania mogą czuć dyskomfort wobec "hakerskiej" natury Notebooków, ale muszę Was zapewnić: częścią pracy z AI jest komfort bycia Naukowcem. Jako Naukowiec, wiele tu eksploracji i eksperymentowania. A Notebooki są idealne do tego rodzaju aktywności.

Notebook to plik z rozszerzeniem ".ipynb", co oznacza IPython Notebook - wczesną nazwę dla tych plików.

## Briefing o Notebookach w Cursorze

Najpierw briefing o tym, jak to wszystko się łączy, oraz jak stworzyć i uruchomić notebook w Cursorze:

https://chatgpt.com/share/6806291a-25f0-8012-a08b-057acb5045ae

## Szerszy przewodnik po Notebookach z przykładami

Notebook to plac zabaw Data Science, gdzie łatwo możesz pisać kod i badać wyniki. To idealne środowisko do:
- Badań i rozwoju (R&D)
- Prototypowania
- Nauki (to my!)

Notebook składa się z serii kwadratowych pól zwanych "komórkami" (cells). Niektóre z nich zawierają tekst, jak ta komórka, a niektóre zawierają kod, jak komórka poniżej.

Najpierw może być konieczne kliknięcie przycisku `Select Kernel` w prawym górnym rogu, a następnie wybranie `venv (Python 3.12.x)` lub podobnego.

Kliknij w komórkę z kodem i naciśnij `Shift + Return` (lub `Shift + Enter`), żeby uruchomić kod i wyświetlić wynik.

Zrób to teraz dla komórki poniżej:

```python
# Click anywhere in this cell and press Shift + Return

2 + 2
```

## Gratulacje!

Teraz uruchom kolejną komórkę, która ustawia wartość, a następnie komórki po niej, żeby wyświetlić tę wartość.

```python
# Set a value for a variable

favorite_fruit = "bananas"
```

```python
# The result of the last statement is shown after you run it

favorite_fruit
```

```python
# Use the variable

print(f"My favorite fruit is {favorite_fruit}")
```

```python
# Now change the variable

favorite_fruit = f"anything but {favorite_fruit}"
```

## Teraz wróć i uruchom ponownie komórkę z instrukcją print, dwie komórki wstecz

Widzisz, że wypisuje coś innego, mimo że favorite_fruit zostało zmienione dalej w notebooku?

Kolejność, w jakiej kod pojawia się w notebooku, nie ma znaczenia. Liczy się kolejność, w jakiej kod jest **wykonywany**. Za tym notebookiem stoi proces Pythona, w którym zmieniane są zmienne.

To zaskakuje niektóre osoby, gdy po raz pierwszy używają notebooków.

```python
# Then run this cell twice, and see if you understand what's going on

print(f"My favorite fruit is {favorite_fruit}")

favorite_fruit = "apples"
```

# Wyjaśnienie 'kernela'

Za tym notebookiem stoi proces Pythona, który wykonuje każdą komórkę, gdy ją uruchamiasz. Ten proces Pythona jest znany jako Kernel. Każdy notebook ma swój własny, oddzielny Kernel.

Możesz kliknąć przycisk powyżej "Restart Kernel".

Jeśli następnie spróbujesz uruchomić kolejną komórkę, dostaniesz błąd, bo favorite_fruit nie jest już zdefiniowane. Będziesz musiał uruchomić komórki od początku notebooka ponownie. Wtedy kolejna komórka powinna zadziałać poprawnie.

```python
print(f"My favorite fruit is {favorite_fruit}")
```

# Dodawanie i usuwanie komórek

Kliknij w tę komórkę, a następnie kliknij przycisk \[+ Code\] na pasku narzędzi powyżej, żeby stworzyć nową komórkę bezpośrednio pod nią. Skopiuj i wklej kod z poprzedniej komórki, a następnie uruchom go! W prawym górnym rogu zaznaczonej komórki znajdują się też ikony do jej usunięcia (kosz).

# Wynik komórki (cell output)

Gdy wykonujesz komórkę, standardowe wyjście oraz wynik ostatniej instrukcji są zapisywane w obszarze bezpośrednio pod kodem, znanym jako 'wynik komórki'. Gdy zapisujesz Notebook z menu plików (albo ctrl+S lub command+S), wynik jest również zapisywany, co czyni go użytecznym zapisem tego, co się wydarzyło.

Możesz to wyczyścić, klikając "Clear All Outputs" na pasku narzędzi. To dobry pomysł, żeby wyczyścić wyniki przed wypchnięciem kodu do repozytorium takiego jak GitHub, w przeciwnym razie pliki mogą być duże i trudniejsze do odczytania.

```python
spams = ["spam"] * 1000
print(spams)

# Might be worth clearing output after running this!
```

# Używanie markdown

Więc co dzieje się z tymi obszarami z tekstem, jak ten? Cóż, w rzeczywistości istnieje inny rodzaj komórki, zwany komórką 'Markdown', do dodawania wyjaśnień takich jak to. Kliknij przycisk [+ Markdown], żeby dodać nową komórkę markdown.

Dodaj kilka komentarzy w formacie Markdown, może kopiując i wklejając stąd:

```
# To jest nagłówek
## To jest podnagłówek
### A to pod-podnagłówek

Lubię Jupyter Lab, bo jest
- Łatwy
- Elastyczny
- Satysfakcjonujący
```

I żeby zamienić to na sformatowany tekst, po prostu naciśnij Shift+Return w komórce.
Kliknij w komórkę i naciśnij ikonę kosza, jeśli chcesz ją usunąć.

# Wykrzyknik

Jest bardzo użyteczna funkcja jupyter labs; możesz wpisać polecenie z ! przed nim w komórce kodu, jak:

!ls
!pwd

I uruchomi to w linii poleceń (tak jakby w Windows Powershell albo Mac Terminal) i wypisze wynik.

```python
# list the current directory

!ls
```

```python
# ping cnn.com - press the stop / interrupt button in the toolbar when you're bored

!ping cnn.com
```

# Drobne rzeczy, na które natrafiamy na kursie

To niekoniecznie funkcja notebooków, ale przydatny pakiet, o którym warto wiedzieć, użyteczny w notebookach.

Pakiet `tqdm` wypisze ładny pasek postępu, jeśli opakujesz nim dowolny obiekt iterowalny.

```python
# Here's some code with no progress bar
# It will take 10 seconds while you wonder what's happpening..

import time

spams = ["spam"] * 1000

for spam in spams:
    time.sleep(0.01)
```

```python
# And now, with a nice little progress bar:

import time
from tqdm import tqdm

spams = ["spam"] * 1000

for spam in tqdm(spams):
    time.sleep(0.01)
```

```python
# On a different topic, here's a useful way to print output in markdown

from IPython.display import Markdown, display

display(Markdown("# This is a big heading!\n\n- And this is a bullet-point\n- So is this\n- Me, too!"))
```

# To wszystko! Znasz już Notebooki / Labs w Cursorze.

## Chcesz być jeszcze bardziej zaawansowany?

Jeśli chcesz zostać profesjonalistą w Jupyter Lab (technologii stojącej za tym), możesz przeczytać ich samouczek [tutaj](https://jupyterlab.readthedocs.io/en/latest/). Ale to nie jest wymagane do naszego kursu; to po prostu dobra technika na naciskanie Shift + Return i cieszenie się wynikiem!
