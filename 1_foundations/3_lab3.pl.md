## Witaj w Labie 3 na Tydzień 1 Dzień 4

Dziś zbudujemy coś z natychmiastową wartością! To początek labu, który potrwa 2 dni.

I zbudujemy ręcznie Pętlę Agenta bez żadnego Frameworka Agentowego..

### Najpierw, trochę przygotowań

W folderze `twin` umieściłem pojedynczy plik `linkedin.pdf` - to pobrany PDF mojego profilu LinkedIn.

Zastąp go swoim! Powinieneś móc go pobrać ze swojego profilu LinkedIn; przejdź na stronę swojego profilu i użyj menu pod swoim imieniem. Jeśli nie masz dostępu do tej funkcji, świetnie sprawdzi się dowolny PDF, taki jak Twoje CV.

Stworzyłem też plik o nazwie `summary.txt` w `twin` - przeczytaj go i zaktualizuj, żeby odzwierciedlał Ciebie.

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/tools.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#00bfff;">Wyszukiwanie pakietów</h2>
            <span style="color:#00bfff;">W tym labie użyjemy wspaniałego pakietu Gradio do szybkiego budowania UI, 
            a także popularnego czytnika PDF PyPDF. Jeśli zastanawiasz się, jak wybierać pakiety do własnych projektów, zobacz Q37 na stronie <a href="https://edwarddonner.com/avatar?q=37">FAQ</a>.
            </span>
        </td>
    </tr>
</table>

```python
# If you don't know what any of these packages do - you can always ask ChatGPT for a guide!

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from IPython.display import Markdown, display
import gradio as gr
import json
```

```python
load_dotenv(override=True)
openai = OpenAI()
```

```python
reader = PdfReader("twin/linkedin.pdf")
linkedin = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text
```

```python
print(linkedin)
```

```python
with open("twin/summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
```

```python
print(summary)
```

## Dygresja: Trzy koncepcje jako przypomnienie

1. System Prompt: część danych wejściowych do LLM, która opisuje ogólny kontekst rozmowy

2. Historia konwersacji: kompletna rozmowa do tej pory

3. Iluzja pamięci: każda wiadomość do LLM jest bezstanowa. Przekazujemy całą dotychczasową rozmowę, żeby stworzyć iluzję, że model pamięta, co zostało powiedziane 30 sekund temu...

__Więcej na ten temat w moim towarzyszącym kursie AI Engineer Core Track (pierwszy tydzień)__

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hi, my name is Ed"}
]
```

```python
response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)
```

```python
messages = [
    {"role": "system", "content": "You are a snarky, witty assistant"},
    {"role": "user", "content": "Hi, my name is Ed"}
]
```

```python
response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)
```

```python
messages = [
    {"role": "system", "content": "You are a snarky, witty assistant"},
    {"role": "user", "content": "What's my name?"}
]
```

```python
response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)
```

```python
messages = [
    {"role": "system", "content": "You are a snarky, witty assistant"},
    {"role": "user", "content": "Hi, my name is Ed"},
    {"role": "assistant", "content": "Well hi there, Ed. It's nice to meet you."},
    {"role": "user", "content": "What's my name?"}
]
```

```python
response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)
```

## Wracamy do głównego wątku!

Mamy profil LinkedIn w zmiennej `linkedin`

Mamy podsumowanie w zmiennej `summary`

Skonstruujmy System Prompt..

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
Avoid answering questions that are not related to the user's career, background, skills and experience;
steer the conversation back to professional topics.

Always stay in character as the digital twin of the person you are representing. Represent the person.

IMPORTANT: If you don't know the answer, say so. Never make up an answer.
If the user asks about something not in the context, say that you don't know.
"""
```

```python
display(Markdown(system_prompt))
```

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "Hi - please tell me about yourself"},
]
```

```python
response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
display(Markdown(response.choices[0].message.content))
```

```python
def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
    return response.choices[0].message.content
```

```python
chat("Please summarize who you are", [])
```

## UWAGA dla tych, którzy nie używają modeli OpenAI

Jeśli używasz modeli innych niż OpenAI, może być konieczne wstawienie tej linii na początku chat():

```python
history = [{"role": h["role"], "content": h["content"]} for h in history]
```

```python
gr.ChatInterface(chat).launch(inbrowser=True)
```

# A teraz - NARZĘDZIA!

Zacznijmy od funkcji...

```python
def record_email_tool(email):
    print(f"Tool called to record an email: {email}")
    with open("emails.txt", "a", encoding="utf-8") as f:
        f.write(email + "\n")
    return "Email received"
```

```python
record_email_tool("test@testy.com")
```

## Krok 1 - napiszmy trochę JSON-a, żeby opisać narzędzie

```python
record_email_tool_json = {
    "name": "record_email_tool",
    "description": "Use this tool to record that a user provided their email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"}
        },
        "required": ["email"],
        "additionalProperties": False
    }
}
```

```python
tools = [{"type": "function", "function": record_email_tool_json}]
```

```python
tools
```

## Krok 2 - nowa funkcja chat()

Tu implementujemy wywołanie narzędzia.

W rzeczywistości jest to trochę toporne. To jak zobaczenie składników wykwintnego przepisu i odkrycie, że składniki okazują się całkiem zwyczajne.

Wywołanie narzędzia to instrukcja "if". W tym przypadku zakodowaliśmy na twardo wszystko, zakładając, że jedynym narzędziem jest narzędzie do maili.

DYGRESJA: Jeśli myślisz - ale czekaj! Powinienem to zapamiętać, żeby móc to zrobić sam! To kluczowy punkt jest taki: to właśnie robią za Ciebie Frameworki Agentowe. W praktyce prawdopodobnie nigdy więcej sam tego nie napiszesz. Jesteśmy osłonięci od tych instrukcji if przez Framework Agentowy. Dlatego często są one określane jako "warstwy abstrakcji".

```python
def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
         
    if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_call = message.tool_calls[0]
            email = json.loads(tool_call.function.arguments).get("email")
            record_email_tool(email)
            messages.append(message)
            messages.append({"role": "tool", "content": "Email recorded", "tool_call_id": tool_call.id})
            response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
            
    return response.choices[0].message.content
```

```python
gr.ChatInterface(chat).launch(inbrowser=True)
```

## Krok 3

Nasza pierwsza w historii Pętla Agenta, zrobiona bez Frameworka Agentowego!

Zmiany:
1. Zamiast zawsze zakładać, że jest tylko 1 wywołanie narzędzia, iterujemy przez narzędzia w pętli for
2. Zmieniono z `if finish_reason=="tool_calls"` na `while finish_reason=="tool_calls"`

```python
def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
         
    while response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            messages.append(message)
            for tool_call in message.tool_calls:
                email = json.loads(tool_call.function.arguments).get("email")
                record_email_tool(email)
                messages.append({"role": "tool", "content": "Email recorded", "tool_call_id": tool_call.id})
            response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=tools)
            
    return response.choices[0].message.content
```

```python
gr.ChatInterface(chat).launch(inbrowser=True)
```

# Gratulacje!

Właśnie zaimplementowałeś Asystenta AI z Narzędziami.
I ręcznie skręciłeś Pętlę Agenta, bez potrzeby Frameworka Agentowego.
To wszystko!

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ćwiczenie</h2>
            <span style="color:#ff7800;">1. Dodaj wiele wywołań LLM! Po tym, jak LLM sformułuje swoją odpowiedź, użyj kolejnego wywołania LLM, żeby ocenić, czy jest ona ściśle związana wyłącznie z pracą.<br/><br/>2. Zastosuj to do swojego biznesu! Zrób Asystenta AI, który potrafi odpowiadać na pytania o Twój obszar biznesowy i użyj narzędzia do zapisywania adresów email osób, które chcą się skontaktować.
            </span>
        </td>
    </tr>
</table>
