# Podstawy techniczne

Kluczowe jest, żebyś czuł się swobodnie z podstawowymi pojęciami technicznymi, z którymi pracujemy. To sprawi, że Twoje doświadczenie z całym kursem będzie znacznie lepsze - bardzo frustrujące potrafi być, gdy nie jesteś pewien, co się dzieje.

Te przewodniki powinny zbudować pewność siebie w zakresie technologii, na których pracujemy.

## Temat 1: ChatGPT kontra OpenAI API

### Jaka jest różnica między ChatGPT a GPT API, oferowanymi przez OpenAI?

#### ChatGPT to narzędzie dla użytkownika końcowego. To produkt czatowy zaprojektowany dla konsumentów, którzy są użytkownikami AI.
- Ma darmowy plan, a także płatne plany subskrypcji z dodatkowymi funkcjami.
- Plany subskrypcji dają użytkownikowi niemal nieograniczony dostęp do korzystania z produktu czatowego.

#### API to usługa dostarczana dla inżynierów AI - inżynierów oprogramowania i data scientistów - pracujących nad innymi produktami komercyjnymi.
- Pozwala osobom technicznym, takim jak Ty i ja, na dostęp do bazowych modeli (jak "GPT4.1" i "o3"), żebyśmy mogli budować własne produkty.
- Gdybyśmy chcieli, moglibyśmy zbudować własną wersję ChatGPT używając API i pobierać opłaty od naszych użytkowników końcowych.
- Jak większość API, OpenAI pobiera niewielką opłatę na podstawie użycia API. Dla większości przykładów w kursie korzystających z gpt-4o-mini, jest to rzędu 0,001$ za wywołanie API.

### Płacę 20$/miesiąc za ChatGPT - dlaczego muszę płacić więcej za API?

- Mam nadzieję, że teraz jest to jasne. API nie jest dla konsumentów; jest dla inżynierów, żeby budowali własne platformy, za które mogą pobierać opłaty.
- Gdybyś miał dostęp do API w ramach swojej subskrypcji, mógłbyś oferować innym narzędzia ChatGPT po niższej cenie i wyeliminować OpenAI z biznesu!
- Pamiętaj: każde wywołanie API może wymagać 10 000 000 000 000 obliczeń zmiennoprzecinkowych - te obliczenia zużywają energię elektryczną!

Zamiast wywoływać API, możesz uruchamiać modele open source lokalnie, ale zazwyczaj mają one 1000 razy mniej obliczeń - i nawet jeśli to niewiele, to przetwarzanie i tak obciąża Twój rachunek za prąd.

## Temat 2: Robienie zrzutu ekranu

Być może już znasz "robienie zrzutu ekranu" na swoim komputerze, ale jeśli nie (albo jeśli myślisz, że oznacza to zrobienie zdjęcia aparatem...), zapoznaj się z tym samouczkiem:

https://chatgpt.com/share/681f691b-6644-8012-b07d-207c68f259d5

## Temat 3: Zmienne środowiskowe i plik `.env`

Ten samouczek prowadzi Cię przez wszystko, co musisz wiedzieć o plikach .env!

Oczywiście nie musisz dodawać pliku .env do .gitignore, bo ja już to za Ciebie zrobiłem. Ale mam nadzieję, że dobrze wyjaśnia tę kwestię.

https://chatgpt.com/share/68061e89-dd84-8012-829d-9f4506c7baaa

## Temat 4: Podstawy sieci

Ten samouczek omawia sieci i typowe problemy z certyfikatami, VPN-ami, DNS i tym podobnymi.

Sekcje dają podsumowanie; powinieneś poprosić ChatGPT o rozwinięcie dowolnej sekcji, jeśli jest istotna dla Twojej sytuacji.

https://chatgpt.com/share/680620ec-3b30-8012-8c26-ca86693d0e3d

## Temat 5: API i biblioteki klienckie - briefing wprowadzający

W tym kursie bardzo często korzystamy z API!

Kluczowe jest zrozumienie podstaw tego, co się dzieje, gdy wykonujemy wywołanie do API, oraz swobodne posługiwanie się słowami takimi jak "endpoint" i "biblioteka kliencka".

Zapoznaj się z tym przewodnikiem:

https://chatgpt.com/share/68062432-43c8-8012-ad91-6311d4ad5858
