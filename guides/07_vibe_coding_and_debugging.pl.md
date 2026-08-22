# Vibe coding i debugowanie

"Vibe coding" to pieszczotliwe określenie na programowanie z pomocą LLM-ów. Jest szczególnie łatwe i wspaniałe w Cursorze! Ale są pewne dobre techniki, żeby to dobrze działało, które omawiam na kursie. Oto kilka kluczowych wskazówek:

1. Jeśli prosisz LLM taki jak ChatGPT czy Claude o napisanie kodu, umieść aktualną datę w swoim prompcie i poinstruuj LLM, żeby generował kod używający najnowszych wersji API. To szczególnie ważne w przypadku OpenAI API! ChatGPT często próbuje używać przestarzałych wersji własnego API...

2. Również w swoich promptach proś LLM-y, żeby kod był tak krótki i prosty, jak to możliwe. LLM-y wydają się uwielbiać dodawać mnóstwo dodatkowych, niepotrzebnych sprawdzeń, które zaśmiecają kod i utrudniają znalezienie problemów.

3. Zadaj to samo pytanie kilku LLM-om i wybierz odpowiedź, która jest najjaśniejsza i najprostsza.

4. Podobnie: weź odpowiedź od jednego LLM-a i poproś inny LLM o zweryfikowanie jej poprawności oraz tego, czy mogłaby być prostsza lub jaśniejsza.

5. Poproś LLM o podanie 3 wariantów rozwiązania problemu i wybierz ten, który jest najjaśniejszy.

## Vibe Coding dla większego projektu

Staraj się unikać sytuacji, w której LLM generuje 100-200 linii kodu lub więcej; będzie Ci bardzo trudno to zdebugować i zrozumieć, co idzie nie tak (chyba że masz już odpowiednią wiedzę).

Zamiast tego: zacznij od rozbicia swojego problemu na małe, niezależnie testowalne kroki, z których każdy jest stosunkowo niewielki. Jeśli nie jesteś pewien, jak rozbić swój problem - to jest coś, o co możesz poprosić LLM!

Następnie dla każdego z tych bloków budulcowych:
- Użyj powyższych wskazówek, żeby LLM zbudował kod
- Poproś też LLM o napisanie testów, żeby przetestować i zweryfikować kod
- Przetestuj to samodzielnie i upewnij się, że działa poprawnie

To pozwoli Ci budować większy projekt z pewnością siebie.

## Złota zasada: zaczynaj od małego, pracuj przyrostowo!
