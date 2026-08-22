# API LLM-ów i Ollama - poza OpenAI

_WAŻNE: Jeśli nie znasz dobrze API w ogólności oraz zmiennych środowiskowych na swoim PC czy Mac, zapoznaj się z sekcją o API w Przewodniku 4: Podstawy techniczne, zanim przejdziesz do tego przewodnika (tematy 3 i 5 w Przewodniku 4)._

## Kluczowy kontekst do korzystania z modeli innych niż OpenAI - przeczytaj to najpierw!

Przez cały kurs korzystamy z API, żeby łączyć się z najsilniejszymi LLM-ami na świecie.

Firmy stojące za tymi LLM-ami, takie jak OpenAI, Anthropic, Google i DeepSeek, zbudowały endpointy webowe. Wywołujesz ich modele, wykonując żądanie HTTP na adres webowy i przekazując wszystkie informacje o swoich promptach.

Ale byłoby uciążliwe, gdybyśmy musieli budować żądania HTTP za każdym razem, gdy chcemy wywołać API.

Żeby to uprościć, zespół OpenAI napisał narzędzie w Pythonie znane jako "Python Client Library" (biblioteka kliencka Pythona), które opakowuje wywołanie HTTP. Więc piszesz kod w Pythonie, a on wywołuje sieć.

I WŁAŚNIE tym jest biblioteka `openai`.

### Czym jest biblioteka kliencka Pythona `openai`

To:
- Lekkie narzędzie w Pythonie
- Zamienia Twoje żądania w Pythonie na wywołanie HTTP
- Konwertuje wyniki wracające z wywołania HTTP na obiekty Pythona

### Czym NIE jest

- Nie ma w niej żadnego kodu do faktycznego uruchamiania dużego modelu językowego! Żadnego kodu GPT! Po prostu wykonuje żądanie webowe
- Nie ma kodu obliczeń naukowych ani nic szczególnie wyspecjalizowanego dla OpenAI

### Jak jej używać:

```python
# Create an OpenAI python client for making web calls to OpenAI
openai = OpenAI()

# Make the call
response = openai.chat.completions.create(model="gpt-4.1-mini", messages=[{"role":"user", "content": "what is 2+2?"}])

# Print the result
print(response.choices[0].message.content)
```

### Co to robi

Gdy wykonujesz wywołanie w Pythonie: `openai.chat.completions.create()`
Po prostu wykonuje żądanie webowe na ten adres url: `https://api.openai.com/v1/chat/completions`
I konwertuje odpowiedź na obiekty Pythona.

To tyle.

Oto dokumentacja API, jeśli wykonujesz [bezpośrednie żądania HTTP webowe](https://platform.openai.com/docs/guides/text?api-mode=chat&lang=curl)
A oto ta sama dokumentacja API, jeśli używasz [biblioteki klienckiej Pythona](https://platform.openai.com/docs/guides/text?api-mode=chat&lang=python)

## Mając ten kontekst - jak używać innych LLM-ów?

Okazuje się, że to bardzo proste!

Wszystkie pozostałe główne LLM-y mają endpointy API kompatybilne z OpenAI.

Więc OpenAI wyświadczyło wszystkim przysługę: powiedzieli, słuchajcie - możecie wszyscy używać naszego narzędzia do konwersji Pythona na żądania webowe. Pozwolimy wam zmienić narzędzie z wywoływania `https://api.openai/com/v1` na wywoływanie dowolnego adresu webowego, który wskażecie.

I tak możesz używać narzędzia OpenAI nawet do wywoływania modeli, które NIE są od OpenAI, w ten sposób:

`not_actually_openai = OpenAI(base_url="https://somewhere.completely.different/", api_key="another_providers_key")`

Ważne jest, żeby docenić, że ten kod OpenAI to po prostu narzędzie do wykonywania wywołań HTTP do endpointów. Więc mimo że używamy kodu od zespołu OpenAI, możemy go użyć do wywoływania modeli innych niż OpenAI.

Oto wszystkie kompatybilne z OpenAI endpointy od głównych dostawców. Obejmuje to nawet użycie Ollama, lokalnie. Ollama udostępnia endpoint na Twojej lokalnej maszynie i uczynili go również kompatybilnym z OpenAI - bardzo wygodne.

```python
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROK_BASE_URL = "https://api.x.ai/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
```

## Oto przykłady dla Gemini, DeepSeek, Ollama i OpenRouter

### Przykład 1: Używanie Gemini zamiast OpenAI

1. Odwiedź Google Studio, żeby założyć konto: https://aistudio.google.com/
2. Dodaj swój klucz jako GOOGLE_API_KEY do swojego `.env`
3. Dodaj go też po raz drugi jako GEMINI_API_KEY do swojego `.env` - to przyda się później.

Następnie:

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

### Przykład 2: Używanie DeepSeek API zamiast OpenAI (tanio, tylko $2 z góry)

1. Odwiedź DeepSeek API, żeby założyć konto: https://platform.deepseek.com/
2. Będziesz musiał doładować minimalne początkowe saldo $2.
3. Dodaj swój klucz jako DEEPSEEK_API_KEY do swojego `.env`

Następnie:

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

### Przykład 3: Używanie Ollama, żeby było za darmo i lokalnie zamiast OpenAI

Ollama pozwala uruchamiać modele lokalnie; udostępnia na Twojej maszynie API kompatybilne z OpenAI.
Nie ma klucza API dla Ollama; nie ma zewnętrznego podmiotu z Twoją kartą kredytową, więc nie potrzeba żadnego klucza.

1. Jeśli jesteś nowy w Ollama, zainstaluj ją zgodnie z instrukcjami tutaj: https://ollama.com
2. Następnie w terminalu Cursora wykonaj `ollama run llama3.2`, żeby porozmawiać z Llama 3.2
UWAGA: nie używaj llama3.3 ani llama4 - to ogromne modele, nieprzeznaczone do domowych komputerów! Zapełnią Ci dysk.

Następnie:

```python
!ollama pull llama3.2

from openai import OpenAI

OLLAMA_BASE_URL = "http://localhost:11434/v1"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="anything")
response = ollama.chat.completions.create(model="llama3.2", messages=[{"role":"user", "content": "what is 2+2?"}])
print(response.choices[0].message.content)
```

### Przykład 4: Używanie popularnej usługi [OpenRouter](https://openrouter.ai), która ma łatwiejszy proces rozliczeń niż OpenAI

OpenRouter jest bardzo wygodny: daje darmowy dostęp do wielu modeli oraz łatwy dostęp za niewielką opłatą z góry do modeli płatnych.

1. Zarejestruj się na https://openrouter.ai
2. Doładuj minimalne wymagane saldo z góry
3. Dodaj swój klucz jako OPENROUTER_API_KEY do pliku `.env`

Następnie:

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

### Używanie różnych dostawców API z frameworkami agentowymi

Frameworki agentowe ułatwiają przełączanie się między tymi dostawcami. Możesz zmieniać LLM-y i wybierać różne w dowolnym momencie kursu. Poniżej są dodatkowe notatki na temat każdego z nich. Dla OpenAI Agents SDK zobacz sekcję dalej w tym notebooku. Dla CrewAI - omawiamy to na kursie, ale jest to proste: po prostu użyj pełnej ścieżki do modelu, jakiej oczekuje LiteLLM.

## Koszty API

Koszt każdego wywołania API jest naprawdę bardzo niski - większość wywołań do modeli, których używamy na tym kursie, to ułamki centa.

Ale niezwykle ważne jest, żeby zauważyć:

1. Złożony projekt agentowy może obejmować wiele wywołań LLM - być może 20-30 - więc może się to sumować. Ważne jest ustawianie limitów i monitorowanie użycia.

2. W przypadku Agentic AI istnieje ryzyko, że agenci wejdą w pętlę albo wykonają więcej przetwarzania niż zamierzone. Powinieneś monitorować swoje użycie API i nigdy nie ustawiać większego budżetu, niż jesteś komfortowo w stanie zaakceptować. Niektóre API mają ustawienie "auto-doładowania", które może automatycznie obciążać Twoją kartę - zdecydowanie polecam trzymać je wyłączone.

3. Powinieneś wydawać tylko tyle, ile jest dla Ciebie komfortowe. Istnieje darmowa alternatywa w postaci Ollama, której możesz użyć jako zamiennika, jeśli chcesz. DeepSeek, Gemini 2.5 Flash i gpt-4.1-nano są znacząco tańsze.

Pamiętaj, że te wywołania LLM zazwyczaj obejmują biliony obliczeń zmiennoprzecinkowych - ktoś musi zapłacić rachunki za prąd!

### Ollama: darmowa alternatywa dla płatnych API (ale zobacz ostrzeżenie o wersji llama)

Ollama to produkt, który działa lokalnie na Twojej maszynie. Może uruchamiać modele open source i udostępnia na Twoim komputerze endpoint API kompatybilny z OpenAI.

Najpierw pobierz Ollama, odwiedzając:
https://ollama.com

Następnie z Terminala w Cursorze (menu View >> Terminal) uruchom to polecenie, żeby pobrać model:

```shell
ollama pull llama3.2
```

OSTRZEŻENIE: Uważaj, żeby nie używać llama3.3 ani llama4 - to znacznie większe modele, nieodpowiednie dla domowych komputerów.

I teraz, za każdym razem, gdy mamy kod taki jak:
`openai = OpenAI()`
Możesz użyć tego jako bezpośredniego zamiennika:
`openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')`
A także zamienić nazwy modeli takie jak **gpt-4o-mini** na **llama3.2**.

Nie musisz nic umieszczać w pliku .env w tym celu; przy Ollama wszystko działa na Twoim komputerze. Nie wywołujesz zewnętrznego podmiotu w chmurze, nikt nie ma danych Twojej karty kredytowej, więc nie ma potrzeby żadnego tajnego klucza! Kod `api_key='ollama'` powyżej jest wymagany tylko dlatego, że biblioteka kliencka OpenAI oczekuje przekazania api_key, ale wartość jest ignorowana przez Ollama.

Poniżej pełny przykład:

```python
# You need to do this one time on your computer
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

Będziesz musiał wprowadzić podobne zmiany, żeby używać Ollama w ramach dowolnego frameworka agentowego - powinieneś być w stanie wygooglować konkretny przykład albo zapytać mnie.

### OpenRouter: wygodna platforma-brama dla OpenAI i innych

OpenRouter to zewnętrzna usługa, która pozwala połączyć się z szerokim zakresem LLM-ów, w tym OpenAI.

Znana jest z prostszego procesu rozliczeń, który może być łatwiejszy dla niektórych krajów spoza USA.

Najpierw zajrzyj na ich stronę:
https://openrouter.ai/

Następnie rzuć okiem na ich quickstart:
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

Możesz zastąpić go kodem takim jak ten:

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

Będziesz musiał wprowadzić podobne zmiany, żeby używać OpenRouter w ramach dowolnego frameworka agentowego - powinieneś być w stanie wygooglować konkretny przykład albo zapytać mnie.

## OpenAI Agents SDK - szczegółowe instrukcje

Z OpenAI Agents SDK (tygodnie 2 i 6) szczególnie łatwo jest używać dowolnego modelu dostarczonego przez samo OpenAI. Po prostu przekaż nazwę modelu:

`agent = Agent(name="Jokester", instructions="You are a joke teller", model="gpt-4o-mini")`

Możesz też podstawić dowolnego innego dostawcę z API kompatybilnym z OpenAI. Robisz to w 3 krokach, tak:

```python
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
deepseek_client = AsyncOpenAI(base_url=DEEPSEEK_BASE_URL, api_key=deepseek_api_key)
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)
```

A następnie po prostu podajesz ten model, gdy tworzysz Agenta.

`agent = Agent(name="Jokester", instructions="You are a joke teller", model=deepseek_model)`

I możesz użyć podobnego podejścia dla dowolnego innego API kompatybilnego z OpenAI, z tymi samymi 3 krokami:

```python
# extra imports
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Step 1: specify the base URL endpoints where the provider offers an OpenAI compatible API
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROK_BASE_URL = "https://api.x.ai/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Step 2: Create an AsyncOpenAI object for that endpoint
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
grok_client = AsyncOpenAI(base_url=GROK_BASE_URL, api_key=grok_api_key)
groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=groq_api_key)
openrouter_client = AsyncOpenAI(base_url=OPENROUTER_BASE_URL, api_key=openrouter_api_key)
ollama_client = AsyncOpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

# Step 3: Create a model object to provide when creating an Agent
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
grok_3_model = OpenAIChatCompletionsModel(model="grok-3-mini-beta", openai_client=openrouter_client)
llama3_3_model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=groq_client)
grok_3_via_openrouter_model = OpenAIChatCompletionsModel(model="x-ai/grok-3-mini-beta", openai_client=openrouter_client)
llama_3_2_local_model = OpenAIChatCompletionsModel(model="llama3.2", openai_client=ollama_client)
```

### Żeby użyć Azure z OpenAI Agents SDK

Zobacz instrukcje tutaj:
https://techcommunity.microsoft.com/blog/azure-ai-services-blog/use-azure-openai-and-apim-with-the-openai-agents-sdk/4392537

Na przykład tak:
```python
from openai import AsyncAzureOpenAI
from agents import set_default_openai_client
from dotenv import load_dotenv
import os
 
# Load environment variables
load_dotenv(override=True)
 
# Create OpenAI client using Azure OpenAI
openai_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)
 
# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client)
```

## Konfiguracja CrewAI

Oto dokumentacja Crew dotycząca połączeń z LLM z nazwami modeli do użycia dla wszystkich modeli. Jak zauważył student Sadan S. (dziękujemy!), warto wiedzieć, że dla Google trzeba użyć zmiennej środowiskowej `GEMINI_API_KEY` zamiast `GOOGLE_API_KEY`:

https://docs.crewai.com/concepts/llms

A oto ich samouczek z dodatkowymi informacjami:

https://docs.crewai.com/how-to/llm-connections

## Konfiguracja LangGraph

Żeby użyć LangGraph z Ollama (i podobnie dla innych modeli):
https://python.langchain.com/docs/integrations/chat/ollama/#installation

Najpierw dodaj pakiet:
`uv add langchain-ollama`

Następnie w labie wprowadź tę zamianę:
```python
from langchain_ollama import ChatOllama
# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatOllama(model="gemma3:4b")
```

I oczywiście uruchom wcześniej `!ollama pull gemma3:4b` (lub dla wybranego modelu).

Wielkie podziękowania dla Miroslava P. za dodanie tego oraz dla Arvina F. za pytanie!

## LangGraph z innymi modelami

Po prostu zastosuj tę samą receptę co powyżej, ale użyj dowolnego z modeli stąd:
https://python.langchain.com/docs/integrations/chat/

## Frameworki agentowe w tygodniu 5

Tydzień 5 to przegląd kilku frameworków agentowych: Google ADK (z A2A), AWS Strands, Pydantic AI, Microsoft Agent Framework, Agno i Mastra. Każdy z nich ma swój własny sposób konfigurowania, którego modelu i dostawcy używasz.

Po szczegóły dotyczące podmiany na innego dostawcę czy model zobacz plik `SWAP_AI.md` w folderze danego dnia pod `5_agent_frameworks`.

## Warto pamiętać

1. Jeśli chcesz używać Ollama do uruchamiania modeli lokalnie, możesz zauważyć, że mniejsze modele mają trudności z bardziej zaawansowanymi projektami. Będziesz musiał eksperymentować z różnymi rozmiarami i możliwościami modeli, a spora cierpliwość może być potrzebna, żeby znaleźć coś, co dobrze działa. Spodziewam się, że kilka naszych projektów jest zbyt wymagających dla llama3.2. Jako alternatywę rozważ darmowe modele na openrouter.ai albo bardzo tanie modele, niemal darmowe - jak DeepSeek.

2. Modele czatowe często radzą sobie lepiej niż modele rozumujące (Reasoning), bo modele rozumujące potrafią "przemyśleć na siłę" (over-think) niektóre zadania. Ważne jest eksperymentowanie. Większy nie zawsze znaczy lepszy...

3. To trochę mylące, ale istnieje 2 różnych dostawców o podobnie brzmiących nazwach!
- Grok to LLM od X (dawniej Twitter) Elona Muska
- Groq to platforma do szybkiej inferencji modeli open source

Jeden ze studentów zwrócił mi uwagę, że "Groq" powstało pierwsze!
