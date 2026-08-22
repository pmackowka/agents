## Pierwszy duży projekt - Cyfrowy Bliźniak

### Ale najpierw: przedstawiamy Pushover

Pushover to zgrabne narzędzie do wysyłania powiadomień push na Twój telefon.

Jest super łatwe do skonfigurowania i zainstalowania!

Po prostu odwiedź https://pushover.net/ i kliknij 'Login or Signup' w prawym górnym rogu, żeby założyć darmowe konto i stworzyć swoje klucze API.

Po rejestracji, na ekranie głównym kliknij "Create an Application/API Token", nadaj dowolną nazwę (np. Agents) i kliknij Create Application.

Następnie dodaj 2 linie do swojego pliku `.env`:

PUSHOVER_USER=_wstaw klucz, który jest w prawym górnym rogu Twojego ekranu głównego Pushover i prawdopodobnie zaczyna się od u_
PUSHOVER_TOKEN=_wstaw klucz, gdy klikniesz w swoją nową aplikację o nazwie Agents (lub jakąkolwiek inną) i prawdopodobnie zaczyna się od a_

Pamiętaj, żeby zapisać plik `.env` i uruchomić `load_dotenv(override=True)` po zapisaniu, żeby ustawić zmienne środowiskowe.

Na koniec kliknij "Add Phone, Tablet or Desktop", żeby zainstalować na swoim telefonie.

## Uwaga - zmiana w stosunku do filmów

W filmie wdrażam bliźniaka za darmo na HuggingFace Spaces. HuggingFace niedawno przestał to wspierać za darmo!

Jest darmowa alternatywa i wyjaśniam ją oraz podaję instrukcje dalej w tym labie.

```python
# imports

from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
```

```python
# The usual start

load_dotenv(override=True)
openai = OpenAI()
```

```python
# For pushover

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

if pushover_user:
    if pushover_user.startswith("u"):
        print("Pushover user found and looks good")
    else:
        print("Pushover user found but doesn't start with u")
else:
    print("Pushover user not found")

if pushover_token:
    if pushover_token.startswith("a"):
        print("Pushover token found and looks good")
    else:
        print("Pushover token found but doesn't start with a")
else:
    print("Pushover token not found")
```

```python
def push(message):
    print(f"Push: {message}")
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data=payload)
```

```python
push("HEY!!")
```

```python
def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"
```

```python
def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"
```

```python
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional info about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}
```

```python
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False
    }
}
```

```python
tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]
```

```python
tools
```

```python
# This function can take a list of tool calls, and run them. This is the IF statement!!

def handle_tool_calls_with_manual_if(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)

        # THE BIG IF STATEMENT!!!

        if tool_name == "record_user_details":
            result = record_user_details(**arguments)
        elif tool_name == "record_unknown_question":
            result = record_unknown_question(**arguments)

        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results
```

## Używanie wbudowanej funkcji globals() z Pythona

Python ma słownik, który daje nam dostęp do wszystkich funkcji globalnych.

Dygresja: z pewnością gdy będziemy wdrażać, użyjemy tego w bardziej zabezpieczony sposób..

```python
globals()["record_unknown_question"]("this is a really hard question")
```

```python
# This gives us a more elegant way that avoids the IF statement.

def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else "No tool found"
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results
```

```python
reader = PdfReader("twin/linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

with open("twin/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
```

```python
system_prompt = f"""

# Your role

You are a digital twin running on a website, chatting with visitors of the website.
You represent the person who's website you are on.
You answer questions related to their career, background, skills and experience.

Here are the details of the person you are representing:

{summary}

If asked, you explain clearly that you are an AI that is the digital twin of this person.

# Context

Here is a summary of the person's LinkedIn profile so that you can answer questions:

{linkedin}

# Rules

Engage with the user. Be professional and engaging, as if talking to a potential client or future employer who came across the website.
Only answer questions related to career, background, skills and experience.
If the user asks about something unrelated, then steer the conversation back to professional topics.

Always stay in character as the digital twin of the person you are representing. Represent the person.

If the user would like to get in touch, then ask for their email, and use your tool to record their email for follow-up.

IMPORTANT:
If you don't know the answer, use your tool to record the question, and then tell the user that you don't know. Never make up an answer.
"""
```

```python
def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
    while response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
    return response.choices[0].message.content
```

```python
gr.ChatInterface(chat).launch(inbrowser=True)
```

## Zamiana na moduły Pythona

Zamieniłem kod z labu na moduły Pythona; to świetna praktyka po zakończeniu eksperymentów w Notebooku.

Mógłbyś umieścić cały powyższy kod w 1 skrypcie Pythona. Ale lepiej jest zorganizować kod w różne moduły dla różnych zagadnień, i to właśnie zrobiłem:

`context.py` wczytuje dane statyczne i konstruuje System Prompt

`tools.py` zawiera cały kod do zarządzania i wywoływania narzędzi, wraz z powiązanym json

`app.py` zawiera aplikację Gradio i wywołanie OpenAI.

`styles.py` zawiera style do zastosowania w Gradio i został w całości napisany przez Claude Code!

Możesz spróbować zrobić to samodzielnie, a potem porównać z moimi wersjami.

Żeby to wypróbować, otwórz terminal w Cursorze:

`cd 1_foundations`
`cd twin`
`uv run app.py`

# STOP PRASY! Uwaga...

Od 9 lipca 2026 HuggingFace nagle przestał pozwalać na darmowe wdrażanie aplikacji Gradio na HuggingFace Spaces.

To dość paskudna niespodzianka!

Spodziewam się, że mogą się z tego wycofać. W międzyczasie oto darmowa alternatywa: użycie Render.

Kompletne instrukcje znajdziesz w [pliku RENDER_INSTRUCTIONS w tym katalogu](RENDER_INSTRUCTIONS.md)

Jeśli nie masz nic przeciwko płaceniu za HuggingFace, oryginalne instrukcje są poniżej.

A także, oto instrukcje na temat mojego cyfrowego bliźniaka, który działa bardzo tanio na fly.io:
https://edwarddonner.com/avatar

Z moim bliźniakiem możesz mnie nie tylko powiadomić przez Push, ale porozmawiać z prawdziwym mną! Oto film o tym, jak go zrobiłem, wraz z instrukcjami, jeśli też chcesz go zrobić. Zacząłem od tej aplikacji Career Conversations.
https://youtu.be/srlhW4H-Gtg

## Oryginalne instrukcje z HF Spaces (już nie za darmo)

Wdrożymy na HuggingFace Spaces.

Zanim zaczniesz: pamiętaj, żeby zaktualizować pliki w katalogu `twin` - swój profil LinkedIn i summary.txt - żeby mówiły o Tobie!

Sprawdź też, że nie ma pliku README w katalogu twin. Jeśli jest, usuń go. Proces wdrażania sam tworzy nowy plik README w tym katalogu.

## Wdrożenie Część 1: HuggingFace

1. Odwiedź https://huggingface.co i załóż konto
2. Z menu Avatar w prawym górnym rogu wybierz Access Tokens. Wybierz "Create New Token". Nadaj mu uprawnienia WRITE - musi mieć uprawnienia WRITE! Zapisz sobie swój nowy klucz.
3. W Terminalu Cursora uruchom: `uvx hf auth login --token YOUR_TOKEN_HERE`, np. `uvx hf auth login --token hf_xxxxxx`, żeby zalogować się z linii poleceń swoim kluczem. Następnie uruchom `uvx hf auth whoami`, żeby sprawdzić, że jesteś zalogowany
4. Weź swój nowy token i dodaj go do pliku .env: `HF_TOKEN=hf_xxx` na przyszłość

## Wdrożenie Część 2: Push!

1. Wejdź do katalogu twin: `cd 1_foundations`, a potem `cd twin`
2. Z katalogu twin wpisz: `uv run gradio deploy`
3. Postępuj zgodnie z instrukcjami, wybierając wartości domyślne: nazwij go `twin`, wskaż app.py, wybierz cpu-basic jako sprzęt, odpowiedz No na pytanie o potrzebę podania sekretów i "no" na github actions.

### Wdrożenie Część 3: Sekrety

1. Wejdź na https://huggingface.co i kliknij swój Avatar, przejdź do swojego profilu, wybierz Space
2. Przejdź do menu 3 kropek i wybierz Settings
3. Przewiń w dół do sekcji Variables and Secrets
4. Naciśnij "New Secret" (nie New Variable) i wpisz nazwę `OPENAI_API_KEY` oraz wartość swojego klucza z pliku .env (lub użyj odpowiedniego klucza dla swojego LLM). Uważaj, żeby zrobić to poprawnie!
5. Powtórz dla `PUSHOVER_USER` i `PUSHOVER_TOKEN` z Twojego pliku .env
6. Bliżej góry ustawień kliknij "Restart space", żeby go zrestartować
7. Kliknij App blisko góry, żeby wrócić do aplikacji, i po restarcie - ciesz się!

### Osadzanie na innej stronie

Żeby osadzić to na innej stronie, wybierz "Embed this space" z menu trzech kropek.

### Rozwiązywanie problemów

Jeśli dostaniesz błąd gradio, spróbuj otworzyć logi (przycisk obok menu 3 kropek).
Spróbuj dodać więcej informacji debugowych, szczególnie wokół swoich kluczy.

### Ponowne wdrażanie space

Po prostu uruchom `uv run gradio deploy` z katalogu twin. Może być konieczne usunięcie pliku README.md, który Gradio tam utworzyło, jeśli chcesz ponownie nazwać swój space.

### Usuwanie space

Z menu 3 kropek wybierz ekran Settings, a na dole jest opcja Delete.

Więcej informacji o wdrażaniu:

https://www.gradio.app/guides/sharing-your-app#hosting-on-hf-spaces

### Mój Cyfrowy Bliźniak

Więc poświęciłem trochę czasu, żeby przenieść mojego Cyfrowego bliźniaka na wyższy poziom!
Oto on:
https://edwarddonner.com/avatar

Możesz mnie nie tylko powiadomić przez Push, ale porozmawiać z prawdziwym mną! Oto film o tym, jak go zrobiłem, wraz z instrukcjami, jeśli też chcesz go zrobić. Zacząłem od tej aplikacji Career Conversations.
https://youtu.be/srlhW4H-Gtg

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ćwiczenie</h2>
            <span style="color:#ff7800;">• Przede wszystkim, wdróż to dla siebie! To realne, wartościowe narzędzie - CV przyszłości..<br/>
            • Następnie popraw zasoby - dodaj lepszy kontekst o sobie. Jeśli znasz RAG, dodaj bazę wiedzy o sobie.<br/>
            • Dodaj więcej narzędzi! Mógłbyś mieć bazę danych SQL z częstymi Q&A, z której LLM mógłby czytać i do której mógłby pisać?<br/>
            • Wprowadź Ewaluatora z ćwiczenia z Dnia 4 i dodaj inne wzorce agentowe.<br/>
            • Niektórzy studenci dodali integrację z Telegramem, żebyś mógł rozmawiać na żywo z ludźmi na swojej stronie, razem ze swoim bliźniakiem!
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
            <span style="color:#00bfff;">Poza oczywistym (Twoim CV przyszłości) ma to zastosowania biznesowe w każdej sytuacji, gdzie potrzebujesz Asystenta AI z wiedzą dziedzinową i zdolnością do interakcji z prawdziwym światem.
            </span>
        </td>
    </tr>
</table>
