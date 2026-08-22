# Witaj na starcie swojej przygody z Agentic AI

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/stop.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Jesteś gotowy do akcji??</h2>
            <span style="color:#ff7800;">Czy ukończyłeś wszystkie kroki konfiguracji w folderze <a href="../setup/">setup</a>?<br/>
            Czy przeczytałeś <a href="../README.md">README</a>? Wiele częstych pytań ma tam odpowiedź!<br/>
            Czy zajrzałeś do przewodników w folderze <a href="../guides/01_intro.ipynb">guides</a>?<br/>
            Jeśli tak, to jesteś gotowy!!
            </span>
        </td>
    </tr>
</table>

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/tools.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#00bfff;">Ten kod to żywy zasób - miej oko na moje aktualizacje</h2>
            <span style="color:#00bfff;">Regularnie wypycham aktualizacje. Gdy ludzie zadają pytania albo mają problemy, dodaję więcej przykładów i poprawiam wyjaśnienia. W efekcie kod poniżej może nie być identyczny jak w filmach, bo dodałem więcej kroków i lepsze komentarze. Traktuj to jak interaktywną książkę towarzyszącą wykładom.<br/><br/>
            Staram się regularnie wysyłać maile z ważnymi aktualizacjami dotyczącymi kursu. Znajdziesz je w sekcji 'Announcements' na Udemy w lewym panelu bocznym. Możesz też wybrać otrzymywanie moich maili przez ustawienia powiadomień (Notification Settings) na Udemy. Szanuję Twoją skrzynkę i zawsze staram się, żeby moje maile wnosiły wartość!
            </span>
        </td>
    </tr>
</table>

### I pamiętaj, żeby się ze mną skontaktować, jeśli mogę pomóc

Uwielbiam się łączyć: https://www.linkedin.com/in/eddonner/

### Nowy w Notebookach takich jak ten? Zajrzyj do folderu guides!

Tylko sprawdź, czy dodałeś już rozszerzenia Python i Jupyter do Cursora, jeśli jeszcze nie zainstalowane:
- Otwórz rozszerzenia (View >> extensions)
- Wyszukaj python i gdy pojawią się wyniki, kliknij to od ms-python i zainstaluj, jeśli jeszcze nie zainstalowane
- Wyszukaj jupyter i gdy pojawią się wyniki, kliknij to od Microsoftu i zainstaluj, jeśli jeszcze nie zainstalowane
Następnie View >> Explorer, żeby przywrócić File Explorer.

A potem:
1. Kliknij tam, gdzie jest napisane "Select Kernel" blisko prawego górnego rogu, i wybierz opcję `.venv (Python 3.12.12)` lub podobną, która powinna być pierwszym albo najbardziej wyeksponowanym wyborem. Możesz najpierw musieć wybrać "Python Environments".
2. Klikaj w każdą "komórkę" poniżej, zaczynając od komórki bezpośrednio pod tym tekstem, i naciskaj Shift+Enter, żeby uruchomić
3. Baw się dobrze!

Po kliknięciu "Select Kernel", jeśli nie ma opcji takiej jak `.venv (Python 3.12.12)`, zrób co następuje:
1. Na Macu: z menu Cursor wybierz Settings >> VS Code Settings (UWAGA: koniecznie wybierz `VSCode Settings`, nie `Cursor Settings`);
Na Windows PC: z menu File wybierz Preferences >> VS Code Settings (UWAGA: koniecznie wybierz `VSCode Settings`, nie `Cursor Settings`)
2. W pasku wyszukiwania ustawień wpisz "venv"
3. W polu "Path to folder with a list of Virtual Environments" wpisz ścieżkę do katalogu głównego projektu, np. C:\Users\username\projects\agents (na Windows PC) albo /Users/username/projects/agents (na Mac lub Linux).
I spróbuj ponownie.

```python
# First let's do an import. If you get an Import Error, see Q5 and then Q25 here: https://edwarddonner.com/avatar

from dotenv import load_dotenv
```

```python
# Next it's time to load the API keys into environment variables
# If this returns false, see the next cell!

load_dotenv(override=True)
```

### Zaraz, czy to właśnie wypisało `False`??

Jeśli tak, najczęstszym powodem jest to, że nie zapisałeś pliku `.env` po dodaniu klucza! Koniecznie zapisz.

Upewnij się też, że plik `.env` nazywa się dokładnie `.env` i znajduje się w katalogu głównym projektu (`agents`)

Nawiasem mówiąc, Twój plik `.env` może mieć symbol stopu obok siebie w Cursorze po lewej stronie, i to jest w rzeczywistości dobra rzecz: to Cursor mówi Ci "hej, zdaję sobie sprawę, że to plik pełen tajnych informacji, i nie wyślę go do zewnętrznego AI po sugestie zmian, bo Twoje klucze nie powinny być pokazywane nikomu innemu."

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/stop.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ostatnie przypomnienia</h2>
            <span style="color:#ff7800;">1. Jeśli nie czujesz się pewnie ze zmiennymi środowiskowymi albo endpointami webowymi / API, przeczytaj tematy 3 i 5 w tym <a href="../guides/04_technical_foundations.ipynb">przewodniku po podstawach technicznych</a>.<br/>
            2. Jeśli chcesz używać innych AI niż OpenAI, jak Gemini, DeepSeek czy Ollama (za darmo), zobacz pierwszą sekcję w tym <a href="../guides/09_ai_apis_and_ollama.ipynb">przewodniku po API AI</a>.<br/>
            3. Jeśli kiedykolwiek dostaniesz Name Error w Pythonie, zawsze możesz to od razu naprawić; zobacz ostatnią sekcję tego <a href="../guides/06_python_foundations.ipynb">przewodnika po podstawach Pythona</a> i przerób oba samouczki i ćwiczenia.<br/>
            </span>
        </td>
    </tr>
</table>

```python
# Check the key - if you're not using OpenAI, check whichever key you're using! Ollama doesn't need a key.

import os
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set - please head to the troubleshooting guide in the setup folder")
```

```python
# And now - the all important import statement
# If you get an import error - head over to Q5 and Q25 in the FAQ at https://edwarddonner.com/avatar
# Even for other LLM providers like Gemini, you still use this OpenAI import - see Guide 9 for why

from openai import OpenAI
```

```python
# And now we'll create an instance of the OpenAI class
# If you're not sure what it means to create an instance of a class - head over to the guides folder (guide 6)!
# If you get a NameError - head over to the guides folder (guide 6)to learn about NameErrors - always instantly fixable
# If you're not using OpenAI, you just need to slightly modify this - precise instructions are in the AI APIs guide (guide 9)

openai = OpenAI()
```

```python
# Create a list of messages in the familiar OpenAI format

messages = [{"role": "user", "content": "Tell me a fun fact"}]
```

```python
messages
```

```python
# And now call it! Any problems, head to the troubleshooting guide
# This uses GPT 5.4 nano, an incredibly cheap model
# The APIs guide (guide 9) has exact instructions for using even cheaper or free alternatives to OpenAI
# If you get a NameError, head to the guides folder (guide 6) to learn about NameErrors - always instantly fixable

response = openai.chat.completions.create(model="gpt-5.4-nano", messages=messages)
print(response.choices[0].message.content)
```

```python
# And now - let's ask for a question:

question = "Please propose a hard, challenging question to assess someone's IQ. Respond only with the question."
messages = [{"role": "user", "content": question}]
```

```python
# ask it - this uses GPT 5.4 mini, still cheap but more powerful than nano

response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
question = response.choices[0].message.content
print(question)
```

```python
# form a new messages list

messages = [{"role": "user", "content": question}]
messages
```

```python
# Ask the model to answer the hard question

response = openai.chat.completions.create(model="gpt-5.4-mini", messages=messages)
answer = response.choices[0].message.content
print(answer)
```

```python
from IPython.display import Markdown, display

display(Markdown(answer))
```

```python
message = f"""
Here is a question:
{question}

And here is a possible answer that might be correct or incorrect:
{answer}

Please evaluate if the answer is correct or incorrect.
"""

print(message)
```

```python
messages = [{"role": "user", "content": message}]
response = openai.chat.completions.create(model="gpt-5.4", messages=messages)
print(response.choices[0].message.content)
```

# Gratulacje!

To był mały, prosty krok w kierunku Agentic AI, z Twoim nowym środowiskiem!

Następnym razem zrobi się ciekawiej...

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ćwiczenie</h2>
            <span style="color:#ff7800;">Teraz wypróbuj to komercyjne zastosowanie:<br/>
            Najpierw poproś LLM o wybranie obszaru biznesowego, który mógłby być wart zbadania pod kątem szansy dla Agentic AI.<br/>
            Następnie poproś LLM o przedstawienie bolączki (pain-point) w tej branży - czegoś trudnego, co mogłoby dojrzeć do rozwiązania agentowego.<br/>
            Na koniec niech trzecie wywołanie LLM zaproponuje rozwiązanie Agentic AI. <br/>
            Omówimy to na nadchodzących labach, więc nie martw się, jeśli nie jesteś pewien.. po prostu spróbuj!
            </span>
        </td>
    </tr>
</table>

```python
# First create the messages:

messages = [{"role": "user", "content": "Something here"}]

# Then make the first call:

response =

# Then read the business idea:

business_area = response.

# And repeat! In the next message, include the business area within the message
```
