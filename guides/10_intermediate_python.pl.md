# Python na poziomie średniozaawansowanym

## Briefing o bardziej zaawansowanych funkcjach Pythona

Ta sekcja zakłada, że jesteś już na bieżąco z podstawami - a teraz omówimy kilka ważnych funkcji Pythona, których używamy na kursie.

1. Comprehensions (składanie list/słowników)  
2. Generatory  
3. Podklasy, Type Hints, Pydantic  
4. Dekoratory
5. Docker (to nie do końca Python, ale używamy go do uruchamiania kodu Pythona!)



```python
# Najpierw stwórzmy kilka rzeczy:

fruits = ["Apples", "Bananas", "Pears"]

book1 = {"title": "Great Expectations", "author": "Charles Dickens"}
book2 = {"title": "Bleak House", "author": "Charles Dickens"}
book3 = {"title": "An Book By No Author"}
book4 = {"title": "Moby Dick", "author": "Herman Melville"}

books = [book1, book2, book3, book4]
```

# Część 1: List i dict comprehensions


```python
# Wystarczająco proste na start

for fruit in fruits:
    print(fruit)
```


```python
# Zróbmy nową wersję fruits

fruits_shouted = []
for fruit in fruits:
    fruits_shouted.append(fruit.upper())

fruits_shouted
```


```python
# Pewnie już to znasz
# Jest fajna konstrukcja w Pythonie zwana "list comprehension" (składanie list), która to robi:

fruits_shouted2 = [fruit.upper() for fruit in fruits]
fruits_shouted2
```


```python
# Ale może nie wiesz, że można zrobić to samo, żeby tworzyć też słowniki:

fruit_mapping = {fruit: fruit.upper() for fruit in fruits}
fruit_mapping
```


```python
# możesz też użyć instrukcji if, żeby przefiltrować wyniki

fruits_with_longer_names_shouted = [fruit.upper() for fruit in fruits if len(fruit)>5]
fruits_with_longer_names_shouted
```


```python
fruit_mapping_unless_starts_with_a = {fruit: fruit.upper() for fruit in fruits if not fruit.startswith('A')}
fruit_mapping_unless_starts_with_a
```


```python
# Kolejne comprehension

[book['title'] for book in books]
```


```python
# Ten kod zakończy się błędem, bo jedna z naszych książek nie ma autora

[book['author'] for book in books]
```


```python
# Ale to zadziała, bo get() zwraca None

[book.get('author') for book in books]
```


```python
# A ten wariant odfiltruje None

[book.get('author') for book in books if book.get('author')]
```


```python
# A ta wersja zamieni to na set, usuwając duplikaty

set([book.get('author') for book in books if book.get('author')])
```


```python
# I na koniec, ta wersja jest jeszcze ładniejsza
# klamry tworzą set, więc to jest set comprehension

{book.get('author') for book in books if book.get('author')}
```

# Część 2: Generatory

Używamy Generatorów na kursie, bo modele AI mogą strumieniować wyniki z powrotem.

Jeśli nigdy wcześniej nie używałeś Generatorów, zacznij od tego świetnego wprowadzenia od ChatGPT:

https://chatgpt.com/share/672faa6e-7dd0-8012-aae5-44fc0d0ec218

Spróbuj wkleić niektóre z jego przykładów do komórki.


```python
# Najpierw zdefiniuj generator; wygląda jak funkcja, ale ma yield zamiast return

import time

def come_up_with_fruit_names():
    for fruit in fruits:
        time.sleep(1) # myślę o owocu
        yield fruit
```


```python
# Potem go użyj

for fruit in come_up_with_fruit_names():
    print(fruit)
```


```python
# Oto kolejny

def authors_generator():
    for book in books:
        if book.get("author"):
            yield book.get("author")
```


```python
# Użyj go

for author in authors_generator():
    print(author)
```


```python
# Oto to samo napisane z użyciem list comprehension

def authors_generator():
    for author in [book.get("author") for book in books if book.get("author")]:
        yield author
```


```python
# Użyj go

for author in authors_generator():
    print(author)
```


```python
# Oto fajny skrót
# Możesz użyć "yield from", żeby yieldować każdy element iterowalnego obiektu

def authors_generator():
    yield from [book.get("author") for book in books if book.get("author")]
```


```python
# Użyj go

for author in authors_generator():
    print(author)
```


```python
# I na koniec - możemy zamienić list comprehension na set comprehension

def unique_authors_generator():
    yield from {book.get("author") for book in books if book.get("author")}
```


```python
# Użyj go

for author in unique_authors_generator():
    print(author)
```


```python
# A teraz dla zabawy - naciśnij przycisk stop na pasku narzędzi, gdy Ci się znudzi!
# To jakbyśmy zrobili własny Large Language Model... choć niezbyt duży..
# Sprawdź, czy rozumiesz, dlaczego wypisuje literę po literze, zamiast słowo po słowie. Jeśli nie jesteś pewien, spróbuj usunąć słowo kluczowe "from" wszędzie w kodzie.

import random
import time

pronouns = ["I", "You", "We", "They"]
verbs = ["eat", "detest", "bathe in", "deny the existence of", "resent", "pontificate about", "juggle", "impersonate", "worship", "misplace", "conspire with", "philosophize about", "tap dance on", "dramatically renounce", "secretly collect"]
adjectives = ["turqoise", "smelly", "arrogant", "festering", "pleasing", "whimsical", "disheveled", "pretentious", "wobbly", "melodramatic", "pompous", "fluorescent", "bewildered", "suspicious", "overripe"]
nouns = ["turnips", "rodents", "eels", "walruses", "kumquats", "monocles", "spreadsheets", "bagpipes", "wombats", "accordions", "mustaches", "calculators", "jellyfish", "thermostats"]

def infinite_random_sentences():
    while True:
        yield from random.choice(pronouns)
        yield " "
        yield from random.choice(verbs)
        yield " "
        yield from random.choice(adjectives)
        yield " "
        yield from random.choice(nouns)
        yield ". "

for letter in infinite_random_sentences():
    print(letter, end="", flush=True)
    time.sleep(0.02)
```

# Ćwiczenie

Napisz kilka klas Pythona dla przykładu z książkami.

Napisz klasę Book z tytułem i autorem. Dołącz metodę has_author()

Napisz klasę BookShelf z listą książek. Dołącz metodę-generator unique_authors()

# Część 3: Podklasy, Type Hints, Pydantic

Oto kilka szczegółów o Klasach na poziomie średniozaawansowanym od naszego przyjaciela AI, w tym użycie type hints, dziedziczenia i metod klasowych. Obejmuje to przykład z Book.

https://chatgpt.com/share/67348aca-65fc-8012-a4a9-fd1b8f04ba59

A tutaj obszerny tutorial o klasach Pydantic, obejmujący wszystko, co musisz wiedzieć o Pydantic.

https://chatgpt.com/share/68064537-6cfc-8012-93e1-f7dd0932f321

## Część 4: Dekoratory

Oto briefing, z przykładem z OpenAI Agents SDK:

https://chatgpt.com/share/6806474d-3880-8012-b2a2-87b3ee4489da

## Część 5: Docker

Oto wygodny tutorial wprowadzający do Dockera.

W ostatniej sekcji, obejmuje to też odpowiedź na pytanie z Tygodnia 6 - co znaczy uruchomić serwer MCP w Dockerze? Ale możesz zignorować to pytanie, jeśli nie jesteś jeszcze przy tygodniu 6.

https://chatgpt.com/share/6814bc1d-2f3c-8012-9b18-dddc82ea421b


```python
# Musisz zainstalować dockera, żeby uruchomić ten przykład
# To pobierze obraz Dockera dla pythona 3.12, stworzy kontener,
# uruchomi trochę kodu w pythonie i wypisze wynik

!docker run --rm python:3.12 python -c "print(2 + 2)"
```
