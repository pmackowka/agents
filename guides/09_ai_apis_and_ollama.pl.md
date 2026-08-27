# API LLM-ów i Ollama - poza OpenAI

_WAŻNE: Jeśli nie czujesz się jeszcze pewnie z API ogólnie, i ze zmiennymi środowiskowymi na swoim PC albo Macu, przejrzyj sekcję o API w Guide 4 Podstawy techniczne, zanim przejdziesz do tego przewodnika (tematy 3 i 5 w Guide 4)._

## Kluczowy kontekst do używania modeli innych niż OpenAI - przeczytaj to najpierw!

W trakcie kursu używamy API do łączenia się z najsilniejszymi LLM-ami na świecie.

Firmy stojące za tymi LLM-ami, takie jak OpenAI, Anthropic, Google i DeepSeek, zbudowały endpointy webowe. Wywołujesz ich modele, wykonując żądanie HTTP na adres webowy i przekazując wszystkie informacje o swoich promptach.

Ale byłoby to bolesne, gdybyśmy musieli budować żądania HTTP za każdym razem, gdy chcemy wywołać API.

Żeby to uprościć, zespół OpenAI napisał narzędzie w Pythonie znane jako "Python Client Library" (biblioteka kliencka Pythona), która opakowuje wywołanie HTTP. Więc piszesz kod w Pythonie, a on wywołuje sieć.

I WŁAŚNIE tym jest biblioteka `openai`.

### Czym jest biblioteka kliencka Pythona `openai`

To:
- Lekkie narzędzie w Pythonie
- Zamienia Twoje żądania w Pythonie na wywołanie HTTP
- Konwertuje wyniki wracające z wywołania HTTP na obiekty Pythona

### Czym NIE jest

- Nie ma w niej żadnego kodu, który faktycznie uruchamia Large Language Model! Żadnego kodu GPT! Po prostu wykonuje żądanie webowe
- Nie ma tam kodu do obliczeń naukowych, ani niczego szczególnie wyspecjalizowanego dla OpenAI

### Jak jej używać:

```python
# Utwórz klienta Pythona OpenAI do wykonywania wywołań webowych do OpenAI
openai = OpenAI()

# Wykonaj wywołanie
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=[{"role":"user", "content": "what is 2+2?"}])

# Wypisz wynik
print(response.choices[0].message.content)
```

### Co to robi

Gdy wykonujesz wywołanie w Pythonie: `openai.chat.completions.create()`  
Po prostu wykonuje żądanie webowe na ten adres URL: `https://api.openai.com/v1/chat/completions`  
I konwertuje odpowiedź na obiekty Pythona.

To wszystko.

Oto dokumentacja API, jeśli wykonujesz [bezpośrednie żądania webowe HTTP](https://platform.openai.com/docs/guides/text?api-mode=chat&lang=curl)  
A oto ta sama dokumentacja API, jeśli używasz [biblioteki klienckiej Pythona](https://platform.openai.com/docs/guides/text?api-mode=chat&lang=python)

## Mając ten kontekst - jak używać innych LLM-ów?

Okazuje się, że to bardzo łatwe!

Wszystkie inne główne LLM-y mają endpointy API kompatybilne z OpenAI.

I tak OpenAI wyświadczyło wszystkim przysługę: powiedzieli, spójrzcie - wszyscy możecie używać naszego narzędzia do zamiany Pythona na żądania webowe. Pozwolimy Wam zmienić to narzędzie z wywoływania `https://api.openai/com/v1` na wywoływanie dowolnego adresu webowego, jaki wskażecie.

I tak możesz używać narzędzia OpenAI nawet do wywoływania modeli, które NIE są od OpenAI, tak jak tutaj:

`not_actually_openai = OpenAI(base_url="https://somewhere.completely.different/", api_key="another_providers_key")`

Ważne jest, żeby docenić, że ten kod OpenAI to po prostu narzędzie do wykonywania wywołań HTTP do endpointów. Więc mimo że używamy kodu od zespołu OpenAI, możemy go użyć do wywoływania modeli innych niż OpenAI.

Oto wszystkie endpointy kompatybilne z OpenAI od głównych dostawców. Obejmuje to nawet lokalne używanie Ollamy. Ollama dostarcza endpoint na Twojej lokalnej maszynie i też zrobili go kompatybilnym z OpenAI - bardzo wygodnie.

```python
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROK_BASE_URL = "https://api.x.ai/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
```

## Oto przykłady dla Gemini, DeepSeek, Ollama, OpenRouter i Anthropic

### Przykład 1: Używanie Gemini zamiast OpenAI

1. Wejdź na Google Studio, żeby założyć konto: https://aistudio.google.com/  
2. Dodaj swój klucz jako GOOGLE_API_KEY do swojego `.env`  
3. Dodaj go też drugi raz jako GEMINI_API_KEY do swojego `.env` - to przyda się później.

Potem:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
google_api_key = os.getenv("GOOGLE_API_KEY")
gemini = OpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
response = gemini.chat.completions.create(model="gemini-2.5-flash-lite", messages=[{"role":"user", "content": "what is 2+2?"}])
print(response.choices[0].message.content)
```

### Przykład 2: Używanie API DeepSeek zamiast OpenAI (tanie, i tylko $2 na start)

1. Wejdź na DeepSeek API, żeby założyć konto: https://platform.deepseek.com/  
2. Będziesz musiał dodać minimalne początkowe saldo $2.  
3. Dodaj swój klucz jako DEEPSEEK_API_KEY do swojego `.env`  

Potem:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek = OpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)
response = deepseek.chat.completions.create(model="deepseek-chat", messages=[{"role":"user", "content": "what is 2+2?"}])
print(response.choices[0].message.content)
```

### Przykład 3: Używanie Ollamy, żeby było za darmo i lokalnie zamiast OpenAI

Ollama pozwala Ci uruchamiać modele lokalnie; dostarcza API kompatybilne z OpenAI na Twojej maszynie.  
Nie ma klucza API dla Ollamy; nie ma trzeciej strony z Twoją kartą kredytową, więc nie potrzeba żadnego klucza.

1. Jeśli jesteś nowy w Ollamie, zainstaluj ją, postępując zgodnie z instrukcjami tutaj: https://ollama.com   
2. Potem w Terminalu Cursora zrób `ollama run llama3.2`, żeby porozmawiać z Llama 3.2  
UWAGA: nie używaj llama3.3 ani llama4 - to ogromne modele nieprzeznaczone do komputerów domowych! Zapełnią Twój dysk.  

Potem:

```python
!ollama pull llama3.2

from openai import OpenAI

OLLAMA_BASE_URL = "http://localhost:11434/v1"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="anything")
response = ollama.chat.completions.create(model="llama3.2", messages=[{"role":"user", "content": "what is 2+2?"}])
print(response.choices[0].message.content)
```

### Przykład 4: Używanie popularnej usługi [OpenRouter](https://openrouter.ai), która ma prostszy proces rozliczeń, zamiast OpenAI

OpenRouter jest bardzo wygodny: daje Ci darmowy dostęp do wielu modeli, i łatwy dostęp z małym wkładem początkowym do modeli płatnych.

1. Zarejestruj się na https://openrouter.ai
2. Dodaj minimalne wymagane saldo początkowe
3. Dodaj swój klucz jako OPENROUTER_API_KEY do swojego pliku `.env`

Potem:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openrouter = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=openrouter_api_key)
response = openrouter.chat.completions.create(model="openai/gpt-4.1-nano", messages=[{"role":"user", "content": "what is 2+2?"}])
print(response.choices[0].message.content)
```

### Przykład 5: Używanie natywnego SDK Anthropic (Claude) zamiast OpenAI

Anthropic (Claude) różni się od pozostałych dostawców na tej liście: nie ma tu prostego podstawienia `base_url` w bibliotece `openai`. Anthropic ma własne Messages API o innym kształcie niż Chat Completions API OpenAI - m.in. `max_tokens` jest wymagany, `system` to osobny parametr (nie wiadomość w liście `messages`), a odpowiedź to lista bloków treści (`response.content`), a nie `response.choices[0].message.content`. Dlatego zamiast podmieniać `base_url`, używa się natywnej biblioteki `anthropic`.

1. Wejdź na konsolę Anthropic, żeby założyć konto: https://console.anthropic.com/  
2. Będziesz musiał doładować konto niewielką kwotą, żeby móc korzystać z API.  
3. Dodaj swój klucz jako ANTHROPIC_API_KEY do swojego `.env`

Potem:

```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv(override=True)

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
anthropic = Anthropic(api_key=anthropic_api_key)
response = anthropic.messages.create(model="claude-haiku-4-5", max_tokens=1024, messages=[{"role":"user", "content": "ile to jest 2+2?"}])
print(next(block.text for block in response.content if block.type == "text"))
```

### Używanie różnych dostawców API z Agent Frameworkami

Agent Frameworki ułatwiają przełączanie się między tymi dostawcami. Możesz przełączać LLM-y i wybierać różne w dowolnym momencie kursu. Poniżej są dodatkowe notatki o każdym z nich. Dla OpenAI Agents SDK, zobacz sekcję dalej w tym notatniku. Dla CrewAI, omawiamy to na kursie, ale to proste: po prostu użyj pełnej ścieżki do modelu, jakiej oczekuje LiteLLM.

## Koszty API

Koszt każdego wywołania API jest naprawdę bardzo niski - większość wywołań do modeli, których używamy na tym kursie, to ułamki centa.

Ale niezwykle ważne jest, żeby zauważyć:

1. Złożony projekt Agentic może wiązać się z wieloma wywołaniami LLM - może 20-30 - więc to się może sumować. Ważne jest, żeby ustawić limity i monitorować zużycie.

2. Przy Agentic AI istnieje ryzyko, że Agenci wpadną w pętlę albo wykonają więcej przetwarzania niż zamierzone. Powinieneś monitorować zużycie swojego API i nigdy nie ustawiać większego budżetu, niż czujesz się komfortowo. Niektóre API mają ustawienie "auto-refill" (automatyczne doładowanie), które może automatycznie obciążać Twoją kartę - zdecydowanie polecam trzymać to wyłączone.

3. Powinieneś wydawać tylko tyle, ile czujesz się komfortowo. Jest darmowa alternatywa w postaci Ollamy, której możesz użyć jako zamiennika, jeśli chcesz. DeepSeek, Gemini 2.5 Flash i gpt-4.1-nano są znacznie tańsze.

Pamiętaj, że te wywołania LLM zwykle wiążą się z bilionami operacji zmiennoprzecinkowych - ktoś musi zapłacić rachunki za prąd!

### Ollama: Darmowa alternatywa dla płatnych API (ale zobacz Ostrzeżenie o wersji llama)

Ollama to produkt, który działa lokalnie na Twojej maszynie. Może uruchamiać modele open-source i dostarcza na Twoim komputerze endpoint API kompatybilny z OpenAI.

Najpierw pobierz Ollamę, wchodząc na:
https://ollama.com

Potem z Terminala w Cursorze (menu View >> Terminal), uruchom tę komendę, żeby pobrać model:

```shell
ollama pull llama3.2
```

OSTRZEŻENIE: Uważaj, żeby nie używać llama3.3 ani llama4 - to dużo większe modele, nieodpowiednie dla komputerów domowych.

I teraz, za każdym razem, gdy mamy kod taki jak:  
`openai = OpenAI()`  
Możesz użyć tego jako bezpośredniego zamiennika:  
`openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')`  
I też zamień nazwy modeli takie jak **gpt-4o-mini** na **llama3.2**.  

Nie musisz nic wpisywać do swojego pliku .env w tym celu; z Ollamą wszystko działa na Twoim komputerze. Nie dzwonisz do żadnej trzeciej strony w chmurze, nikt nie ma danych Twojej karty kredytowej, więc nie ma potrzeby żadnego tajnego klucza! Kod `api_key='ollama'` powyżej jest wymagany tylko dlatego, że biblioteka kliencka OpenAI oczekuje przekazania api_key, ale wartość jest ignorowana przez Ollamę.

Poniżej pełny przykład:

```python
# Musisz to zrobić raz, na swoim komputerze
!ollama pull llama3.2

from openai import OpenAI
MODEL = "llama3.2"
openai = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

response = openai.chat.completions.create(
 model=MODEL,
 messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

print(response.choices[0].message.content)
```

Będziesz musiał wprowadzić podobne zmiany, żeby użyć Ollamy w dowolnym z Agent Frameworków - powinieneś być w stanie wygooglować dokładny przykład, albo zapytać mnie.

### OpenRouter: Wygodna platforma-brama do OpenAI i innych

OpenRouter to usługa trzeciej strony, która pozwala Ci łączyć się z szeroką gamą LLM-ów, w tym OpenAI.

Znana jest z prostszego procesu rozliczeń, który może być łatwiejszy dla niektórych krajów spoza USA.

Najpierw zajrzyj na ich stronę:  
https://openrouter.ai/

Potem rzuć okiem na ich quickstart:  
https://openrouter.ai/docs/quickstart

I dodaj swój klucz do pliku .env:  
```shell
OPENROUTER_API_KEY=sk-or....
```

I teraz, za każdym razem, gdy masz kod taki jak ten:  
```python
MODEL = "gpt-4o-mini"
openai = OpenAI()
```

Możesz zamienić go na kod taki jak ten:

```python
MODEL = "openai/gpt-4o-mini"
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
openai = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=openrouter_api_key)

response = openai.chat.completions.create(
 model=MODEL,
 messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

print(response.choices[0].message.content)
```

Będziesz musiał wprowadzić podobne zmiany, żeby użyć OpenRouter w dowolnym z Agent Frameworków - powinieneś być w stanie wygooglować dokładny przykład, albo zapytać mnie.

## OpenAI Agents SDK - szczegółowe instrukcje

Z OpenAI Agents SDK (tygodnie 2 i 6), szczególnie łatwo jest użyć dowolnego modelu dostarczanego przez samo OpenAI. Po prostu przekaż nazwę modelu:

`agent = Agent(name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini")`

Możesz też podstawić dowolnego innego dostawcę z API kompatybilnym z OpenAI. Robisz to w 3 krokach, tak:

```python
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)
```

A potem po prostu przekazujesz ten model, gdy tworzysz Agenta.

`agent = Agent(name="Jokester", instructions="You are a joke teller", model=deepseek_model)`

I możesz użyć podobnego podejścia dla dowolnego innego API kompatybilnego z OpenAI, w tych samych 3 krokach:

```python
# dodatkowe importy
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Krok 1: wskaż endpointy base URL, gdzie dostawca oferuje API kompatybilne z OpenAI
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROK_BASE_URL = "https://api.x.ai/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Krok 2: Utwórz obiekt AsyncOpenAI dla tego endpointu
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
grok_client = AsyncOpenAI(base_url=GROK_BASE_URL, api_key=grok_api_key)
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
openrouter_client = AsyncOpenAI(base_url=OPENROUTER_BASE_URL, api_key=openrouter_api_key)
ollama_client = AsyncOpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

# Krok 3: Utwórz obiekt modelu do przekazania podczas tworzenia Agenta
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
grok_3_model = OpenAIChatCompletionsModel(model="grok-3-mini-beta", openai_client=openrouter_client)
llama3_3_model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=groq_client)
grok_3_via_openrouter_model = OpenAIChatCompletionsModel(model="x-ai/grok-3-mini-beta", openai_client=openrouter_client)
llama_3_2_local_model = OpenAIChatCompletionsModel(model="llama3.2", openai_client=ollama_client)
```

### Żeby używać Azure z OpenAI Agents SDK

Zobacz instrukcje tutaj:  
https://techcommunity.microsoft.com/blog/azure-ai-services-blog/use-azure-openai-and-apim-with-the-openai-agents-sdk/4392537

Na przykład tak:
```python
from openai import AsyncAzureOpenAI
from agents import set_default_openai_client
from dotenv import load_dotenv
import os
 
# Załaduj zmienne środowiskowe
load_dotenv(override=True)
 
# Utwórz klienta OpenAI używającego Azure OpenAI
openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)
 
# Ustaw domyślnego klienta OpenAI dla Agents SDK
set_default_openai_client(openai_client)
```

## Konfiguracja CrewAI

Oto dokumentacja Crew dotycząca połączeń LLM z nazwami modeli do użycia dla wszystkich modeli. Jak zauważył kursant Sadan S. (dzięki!), warto wiedzieć, że dla Google trzeba użyć zmiennej środowiskowej `GEMINI_API_KEY` zamiast `GOOGLE_API_KEY`:

https://docs.crewai.com/concepts/llms

A oto ich tutorial z dodatkowymi informacjami:

https://docs.crewai.com/how-to/llm-connections

## Konfiguracja LangGraph

Żeby użyć LangGraph z Ollamą (i postępować podobnie dla innych modeli):  
https://python.langchain.com/docs/integrations/chat/ollama/#installation

Najpierw dodaj pakiet:  
`uv add langchain-ollama`

Potem w labie zrób tę zamianę:   
```python
from langchain_ollama import ChatOllama
# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatOllama(model="gemma3:4b")
```

I oczywiście uruchom wcześniej `!ollama pull gemma3:4b` (albo jaki tam model).

Wielkie dzięki dla Miroslava P. za dodanie tego, i dla Arvina F. za pytanie!

## LangGraph z innymi modelami

Po prostu postępuj według tego samego przepisu co powyżej, ale użyj dowolnego z modeli stąd:  
https://python.langchain.com/docs/integrations/chat/


## Agent Frameworki z Tygodnia 5

Tydzień 5 to objazd po kilku agent frameworkach: Google ADK (z A2A), AWS Strands, Pydantic AI, Microsoft Agent Framework, Agno i Mastra. Każdy z nich ma swój własny sposób konfigurowania, jakiego modelu i dostawcy używasz.

Po szczegóły podmiany na inny model albo dostawcę, zobacz plik `SWAP_AI.md` w folderze danego dnia pod `5_agent_frameworks`.

## Warto pamiętać

1. Jeśli chcesz użyć Ollamy do uruchamiania modeli lokalnie, możesz odkryć, że mniejsze modele mają problemy z bardziej zaawansowanymi projektami. Będziesz musiał eksperymentować z różnymi rozmiarami i możliwościami modeli, i może być potrzeba sporo cierpliwości, żeby znaleźć coś, co dobrze działa. Spodziewam się, że kilka naszych projektów jest zbyt wymagających dla llama3.2. Jako alternatywę rozważ darmowe modele na openrouter.ai, albo bardzo tanie modele, niemal darmowe - jak DeepSeek.

2. Modele Chat często radzą sobie lepiej niż modele Reasoning, bo modele Reasoning mogą "przemyśleć na zapas" niektóre zadania. Ważne jest, żeby eksperymentować. Większy nie zawsze znaczy lepszy...

3. To mylące, ale są 2 różni dostawcy, którzy brzmią podobnie!  
- Grok to LLM z X Elona Muska
- Groq to platforma do szybkiej inferencji modeli open source

Kursant zwrócił mi uwagę, że "Groq" było pierwsze!



