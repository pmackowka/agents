# Przewodnik przetrwania w debugowaniu

## Kluczem jest konsekwentne odtworzenie problemu w 5-10 liniach kodu

Napotkanie wyjątku może czasem być dość frustrujące, szczególnie jeśli nie jesteś pewien, jak do tego podejść. Ale właśnie wtedy dzieje się najlepsza nauka! Dochodzenie do sedna trudnych problemów to świetny sposób na naukę i może być całkiem satysfakcjonujące.

Ale jestem tu, żeby pomóc, jeśli nie dasz rady!

### Wstęp

Oto briefing o wyjątkach, stack trace'ach, obsłudze wyjątków i innych rzeczach:

https://chatgpt.com/share/6806383c-ab38-8012-b21f-61af665bb900

Zobacz też [ten przewodnik](https://chatgpt.com/share/681f691b-6644-8012-b07d-207c68f259d5), jeśli nie jesteś pewien, jak robić zrzuty ekranu.

### Formuła na debugowanie: odtwórz w 10 liniach kodu

Świetne debugowanie to zarówno sztuka, jak i nauka. Najlepszy sposób, żeby to opanować, to praktyka! Ale oto najważniejsze zasady:

1. Odtwórz
Odtwórz swój problem, konsekwentnie.

2. Uprość
Zredukuj swój problem do najprostszego możliwego sposobu jego odtworzenia. Nie powiem Ci, ilu ludzi przysłało mi ponad 100 linii kodu i powiedziało "Ed, to nie działa, napraw to proszę". Tak to nie działa! Pierwsze, co bym spróbował, to zredukować to do sedna problemu - najlepiej w 10-20 liniach kodu lub mniej. W jednym przypadku pokazałem studentowi, jak odtworzyć problem w 2 liniach kodu!

_Rzecz w tym, że **Tobie** jest to zrobić dużo łatwiej niż komukolwiek innemu._ Więc choć może to być żmudne, to niemal zawsze najlepszy sposób na start. Zredukuj do kilku linii kodu. I nawiasem mówiąc, gdy to zrobisz, często sam odkryjesz problem!

3. Zdobądź pomoc
Gdy już odtworzyłeś problem zaledwie kilkoma liniami kodu i nadal nie widzisz, co się dzieje - poproś o pomoc! Warto oczywiście zapytać ChatGPT i przyjaciół; daj im krótki przykład i pełny stack trace.

I odezwij się do mnie! Jestem tu, żeby Twoje doświadczenie nauki było jak najlepsze, a jeśli utkniesz, pomogę Ci się z tego wydostać.

### Najlepszy sposób pracy ze mną dla najszybszych napraw...

1. Uprość problem tak bardzo, jak to możliwe, z łatwym sposobem odtworzenia
2. Dołącz pełny stack trace oraz zrzut ekranu, nie zdjęcie (zobacz [ten przewodnik](https://chatgpt.com/share/681f691b-6644-8012-b07d-207c68f259d5), jeśli nie jesteś pewien, jak robić zrzuty ekranu)
3. Napisz do mnie na ed@edwarddonner.com. Albo najlepiej: jeśli używałeś kiedyś Google Colab, to naprawdę świetny sposób, żeby podzielić się problemem, bo będzie identyczny do odtworzenia dla mnie, a ja mogę go naprawić i podzielić się poprawką bezpośrednio z Tobą.

Nie mogę się doczekać, żeby Ci pomóc!
