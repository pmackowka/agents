## Witaj w Drugim Labie - Tydzień 1, Dzień 3

Dziś popracujemy z mnóstwem modeli! To sposób, żeby oswoić się z API.

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/stop.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ważna kwestia - przeczytaj koniecznie</h2>
            <span style="color:#ff7800;">Sposób, w jaki z Tobą współpracuję, może różnić się od innych kursów, które brałeś. Wolę nie pisać kodu, podczas gdy Ty patrzysz. Zamiast tego uruchamiam Jupyter Labs, tak jak to, i daję Ci intuicję co do tego, co się dzieje. Moja sugestia jest taka, żebyś sam uważnie to uruchomił, <b>po</b> obejrzeniu wykładu. Dodaj instrukcje print, żeby zrozumieć, co się dzieje, a potem wymyśl własne warianty. Zobacz Q37 w <a href="https://edwarddonner.com/avatar?q=37">FAQ</a>, jak skonfigurować osobny projekt do swojej pracy.<br/><br/>Jeśli masz czas, byłbym zachwycony, gdybyś zgłosił PR ze zmianami w folderze community_contributions - instrukcje w zasobach. Jeśli masz konto Github, wykorzystaj je, żeby pokazać swoje warianty. To nie tylko kluczowa praktyka, ale też pokazuje Twoje umiejętności innym, w tym może przyszłym klientom czy pracodawcom...<br/>A jeśli napiszesz o tym na LinkedIn i oznaczysz mnie, to włączę się, żeby wzmocnić Twoje osiągnięcie. Jeśli widzisz innych studentów, którzy to publikują, im też daj wsparcie.
            </span>
        </td>
    </tr>
</table>

```python
# Start with imports - ask the Cursor Agent to explain any package that you don't know

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
```

```python
# Always remember to do this!
load_dotenv(override=True)
```

```python
# Print the key prefixes to help with any debugging

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
grok_api_key = os.getenv('GROK_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set (and this is optional)")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
    print("Google API Key not set (and this is optional)")

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
else:
    print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
    print("Groq API Key not set (and this is optional)")

if grok_api_key:
    print(f"Grok API Key exists and begins {grok_api_key[:4]}")
else:
    print("Grok API Key not set (and this is optional)")

if openrouter_api_key:
    print(f"OpenRouter API Key exists and begins {openrouter_api_key[:6]}") 
else:
    print("OpenRouter API Key not set (and this is optional)")
```

```python
request = """
Please come up with a challenging, nuanced question with a succinct answer,
that I can ask a number of LLMs to evaluate their intelligence.
Not a mathematical puzzle, but more of a thought-provoking question that requires intelligent insight.
Include in your question that the answer must be short.
"""
request += "Answer only with the question, no explanation."
messages = [{"role": "user", "content": request}]
```

```python
messages
```

```python
openai = OpenAI()

response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
question = response.choices[0].message.content
display(Markdown(question))
```

## Wywoływanie LLM-ów od wielu dostawców

Zamierzamy wywołać LLM-y od wielu innych dostawców.
Wszystkie oferują endpointy API kompatybilne z OpenAI, jak wyjaśniono w Przewodniku 9 w folderze guides.
Więc możemy po prostu użyć tych endpointów tak, jakbyśmy używali OpenAI.

Uwaga:

Użyję mnóstwa LLM-ów od różnych dostawców, ale Ty nie musisz! To tylko po to, żeby pokazać ich możliwości.

```python
# OpenAI Compatible URLs

ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROK_BASE_URL = "https://api.x.ai/v1"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
```

```python
# OpenAI client libraries with the right base_url and key
# If this surprises you, please see Guide 9 in the Guides folder!

anthropic = OpenAI(api_key=anthropic_api_key, base_url=ANTHROPIC_BASE_URL)
deepseek = OpenAI(api_key=deepseek_api_key, base_url=DEEPSEEK_BASE_URL)
gemini = OpenAI(api_key=google_api_key, base_url=GEMINI_BASE_URL)
groq = OpenAI(api_key=groq_api_key, base_url=GROQ_BASE_URL)
grok = OpenAI(api_key=grok_api_key, base_url=GROK_BASE_URL)
openrouter = OpenAI(api_key=openrouter_api_key, base_url=OPENROUTER_BASE_URL)
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")
```

```python
competitors = []
answers = []
messages = [{"role": "user", "content": question}]
```

```python
def record(model_name, answer):
    competitors.append(model_name)
    answers.append(answer)
    display(Markdown(answer))
```

```python
# The API we know well
# Reasoning effort can be none, low, medium, high, or xhigh

model_name = "gpt-5.4-nano"

response = openai.chat.completions.create(model=model_name, messages=messages, reasoning_effort="none")
answer = response.choices[0].message.content

record(model_name, answer)
```

```python
model_name = "claude-sonnet-4-6"

response = anthropic.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

record(model_name, answer)
```

```python
model_name = "gemini-3.1-flash-lite"

response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

record(model_name, answer)
```

```python
model_name = "deepseek-v4-flash"

response = deepseek.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

record(model_name, answer)
```

```python
model_name = "openai/gpt-oss-120b"

response = groq.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)
```

```python
model_name = "moonshotai/kimi-k2.6"

response = openrouter.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

record(model_name, answer)
```

## W kolejnej komórce użyjemy Ollama

Ollama uruchamia lokalną usługę webową, która daje endpoint kompatybilny z OpenAI,
i uruchamia modele lokalnie za pomocą wydajnego kodu w C++.

Jeśli nie masz Ollama, zainstaluj ją tutaj, odwiedzając https://ollama.com, a potem naciskając Download i postępując zgodnie z instrukcjami.

Po instalacji powinieneś móc odwiedzić tutaj: http://localhost:11434 i zobaczyć komunikat "Ollama is running"

Może być konieczny restart Cursora (a może i reboot). Następnie otwórz Terminal (control+\`) i uruchom `ollama serve`

Przydatne polecenia Ollama (uruchom je w terminalu albo z wykrzyknikiem w tym notebooku):

`ollama pull <model_name>` pobiera model lokalnie
`ollama ls` wylistowuje wszystkie pobrane przez Ciebie modele
`ollama rm <model_name>` usuwa wskazany model z Twoich pobrań

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/stop.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Bardzo ważne - zignoruj mnie na własne ryzyko!</h2>
            <span style="color:#ff7800;">Wiele modeli na Ollama jest ZDECYDOWANIE za dużych na Twój domowy komputer. Koniecznie przeglądaj modele na stronie Ollama. Staraj się używać modeli o rozmiarze 3GB lub mniej, chyba że wiesz lepiej; llama3.2 to świetny pierwszy wybór. Nie wybieraj modeli kończących się na :cloud; to coś innego (usługa inferencji w chmurze, jak Groq).
            </span>
        </td>
    </tr>
</table>

```python
!ollama pull llama3.2
```

```python
import requests
requests.get('http://localhost:11434').content
```

```python
import requests
models = requests.get('http://localhost:11434/v1/models').json()
for model in models.get("data"):
    print(model.get("id"))
```

```python
model_name = "llama3.2:1b"

response = ollama.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

record(model_name, answer)
```

```python
model_name = "gpt-oss:latest"

response = ollama.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)
```

```python
model_name = "gemma4:latest"

response = ollama.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)
```

```python
# So where are we?

print(len(competitors))
print(competitors)
print(answers)
```

```python
# It's nice to know how to use "zip"
for competitor, answer in zip(competitors, answers):
    print(f"Competitor: {competitor}\n\n{answer}")
```

```python
# Let's bring this together - note the use of "enumerate"

together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"
```

```python
print(together)
```

```python
judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response for clarity and strength of argument, and rank them in order of best to worst.
Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""
```

```python
print(judge)
```

```python
judge_messages = [{"role": "user", "content": judge}]
```

## A teraz czas na Grok!

Reklamowany jako "Najbardziej prawdoszukający duży model językowy na świecie".. więc użyjmy go jako naszego LLM-a w roli sędziego

```python
# Judgement time!
# Grok is "The most truth-seeking large language model in the world."

model_name = "grok-4.3"

response = grok.chat.completions.create(model=model_name, messages=judge_messages)
results = response.choices[0].message.content
print(results)
```

```python
# OK let's turn this into results!

results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")
```

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ćwiczenie</h2>
            <span style="color:#ff7800;">Który wzorzec (wzorce) tu wykorzystano? Spróbuj to zaktualizować, żeby dodać kolejny wzorzec projektowy agentowy.
            </span>
        </td>
    </tr>
</table>

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/business.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#00bfff;">Implikacje komercyjne</h2>
            <span style="color:#00bfff;">Tego rodzaju wzorce - żeby wysłać zadanie do wielu modeli i ocenić wyniki,
            są powszechne tam, gdzie trzeba poprawić jakość odpowiedzi LLM. To podejście można uniwersalnie zastosować
            do projektów biznesowych, gdzie dokładność jest kluczowa.
            </span>
        </td>
    </tr>
</table>
