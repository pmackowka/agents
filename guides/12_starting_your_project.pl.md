## Jak zacząć pracę nad swoim pomysłem

Więc masz pomysł na coś, co chciałbyś zbudować.

GRATULACJE! To najważniejsza część już zrobiona. Pomysł to wszystko!

Ale teraz nie jesteś pewien, od czego zacząć. Dostaję mnóstwo pytań na ten temat.

Chcę dać Ci trzy kluczowe rady.

## Rada 1: Bądź Naukowcem

Bycie inżynierem AI wymaga noszenia 2 kapeluszy: bycia Inżynierem Oprogramowania i bycia Data Scientistem.

Na początku swojego projektu kluczowe jest, żeby zdjąć kapelusz Inżyniera Oprogramowania i zdecydowanie założyć kapelusz Data Scientista.

Wiele osób z backgroundem inżynierii oprogramowania (w tym ja!) ma z tym problem. To powszechne, że ludzie wpadają w swoją strefę komfortu, zadając pytania o architekturę, design, pipeline'y danych, skalowalność, wdrożenie.

To wszystko świetne pytania, ale nie są to te kluczowe na tym wczesnym etapie. Nie są to trudne pytania. Nie zadecydują o sukcesie ani porażce Twojego pomysłu.

Dla kluczowych pytań musisz być Naukowcem.

Zapytaj siebie:
1. Jak ocenisz sukces swojego modelu? Co będziesz mierzyć?
2. Jakie dane masz, a jakich potrzebujesz?
3. Jak możesz zbudować małe prototypy, żeby przetestować różne techniki i zrozumieć wydajność modelu?

Najpierw zajmij się pytaniami naukowymi - co możesz osiągnąć z LLM-ami i jak.

I polecam zacząć w Notebooku, zanim zaczniesz pracować w modułach Pythona, żeby zmusić się do działania w tym naukowym nastawieniu.

Jest to jeszcze bardziej kluczowe w przypadku projektów agentowych. Może być kuszące, żeby narysować wielki diagram architektury Agentów pokazujący, jak Twoje agenty będą współpracować, jak diagram techniczny. Ale to myślenie jak Inżynier Oprogramowania. Polecam podejść do tego inaczej; eksperymentuj z różnymi podejściami, badaj, co dobrze działa, testuj hipotezy i iteruj.

## Rada 2: Przyjmij R&D

OK, więc to dość podobne do Rady 1, ale warto to powtórzyć!

Często dostaję pytania typu: "Ed, chcę zbudować takie rozwiązanie. Czy powinienem użyć modelu A, B, czy C? Czy powinienem użyć Agentów, RAG, czy fine-tuningu?"

Moja odpowiedź niemal zawsze brzmi:
- Powinieneś zrobić wszystko powyższe! Kluczem jest eksperymentowanie; (a) wymyśl kryteria oceny, (b) zbuduj wyselekcjonowany zbiór danych, (c) przetestuj różne pomysły i zobacz, jak sobie radzą
- Często mam przeczucie, co zadziała najlepiej, ale moje przeczucie często się myli! Nie ufaj mi: wypróbuj to sam
- Po prostu nie ma substytutu dla eksperymentowania.

## Rada 3: Marz wielko, ale zaczynaj OD MAŁEGO!

Często też studenci przysyłają mi 200-300 linii kodu, mówiąc: "Ed, to nie działa, napraw to proszę". 😂

Jak mówię w przewodniku o debugowaniu - tak to nie działa!

Kiedy zaczynasz projekty, kluczowe jest, żeby zacząć od małego i prostego. Dopracuj każdy prompt; pracuj w szczegółach nad każdym krokiem. Upewnij się, że każde wywołanie LLM działa tak, jak chcesz, i iteruj nad danymi wejściowymi, aż odpowiedzi będą spójne i niezawodne.

Jeśli zawsze pracujesz przyrostowo, z małymi, testowalnymi blokami budulcowymi, powinieneś mieć pełną jasność co do tego, co się dzieje.

I oczywiście uwielbiam pomagać ludziom w projektach i świetnie jest pomagać naprawiać problemy. Ale jeśli podejdziesz do swojego projektu przyrostowo, zawsze powinieneś mieć jasność co do tego, co dokładnie nie działa - a wtedy bardzo efektywnie mogę Ci pomóc.

# Podsumowując

Prawdopodobnie zauważyłeś wspólny motyw w tych 3 radach. Dla osób bez backgroundu w Data Science może to być dziwne - podchodzić do problemów w tak doraźny sposób; wydaje się to "hakerskie" i niezbyt satysfakcjonujące. Ale moim zdaniem to pojedyncza najważniejsza umiejętność do zdobycia, żeby być skutecznym inżynierem AI: komfort wobec niepewności, czerpanie radości z eksperymentów i przyjęcie roli Naukowca.
