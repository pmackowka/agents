# "Ale czekaj... to jeszcze nie wszystko"

## Bardziej widoczna Pętla Agenta

Cyfrowy Bliźniak zawierał Pętlę Agenta. Ale działała ona za kulisami, uruchamiając się za każdym razem, gdy użytkownik zadawał wiadomość. Używając swoich narzędzi, a potem odpowiadając. Nie było w tym zbyt wiele... pętlowatości.

### Dodanie 2 kolejnych składników, żeby uczynić to bardziej realnym

Zróbmy Pętlę Agenta z kilkoma znajomymi funkcjami zapożyczonymi z Claude Code:

1. Terminalowy UI (TUI)
2. Narzędzie Checklist, żeby wywoływać i śledzić wiele wywołań narzędzi

```python
# Start with some imports - rich is a library for making formatted text output in the terminal

from rich.console import Console
from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv(override=True)
```

```python
def show(text):
    try:
        Console().print(text)
    except Exception:
        print(text)
```

```python
openai = OpenAI()
```

```python
# Some lists!

checklist = []
completed = []
```

```python
def get_checklist_report() -> str:
    result = ""
    for index, item in enumerate(checklist):
        if completed[index]:
            result += f"Checklist #{index + 1}: [green][strike]{item}[/strike][/green]\n"
        else:
            result += f"Checklist #{index + 1}: {item}\n"
    show(result)
    return result
```

```python
get_checklist_report()
```

```python
def create_checklist(descriptions: list[str]) -> str:
    checklist.extend(descriptions)
    completed.extend([False] * len(descriptions))
    return get_checklist_report()
```

```python
def mark_complete(index: int, completion_notes: str) -> str:
    if 1 <= index <= len(checklist):
        completed[index - 1] = True
    else:
        return "No checklist at this index."
    Console().print(completion_notes)
    return get_checklist_report()
```

```python
checklist, completed = [], []

create_checklist(["Buy groceries", "Finish week 1", "Eat banana"])
```

```python
mark_complete(1, "bought")
```

```python
create_checklist_json = {
    "name": "create_checklist",
    "description": "Add new checklist from a list of descriptions and return the full list",
    "parameters": {
        "type": "object",
        "properties": {
            "descriptions": {
                'type': 'array',
                'items': {'type': 'string'},
                'title': 'Descriptions of checklist items'
                }
            },
        "required": ["descriptions"],
        "additionalProperties": False
    }
}
```

```python
mark_complete_json = {
    "name": "mark_complete",
    "description": "Mark complete the checklist item at the given position (starting from 1) and return the full list",
    "parameters": {
        'properties': {
            'index': {
                'description': 'The 1-based index of the checklist item to mark as complete',
                'title': 'Index',
                'type': 'integer'
                },
            'completion_notes': {
                'description': 'Notes about how you completed the checklist item in rich console markup',
                'title': 'Completion Notes',
                'type': 'string'
                }
            },
        'required': ['index', 'completion_notes'],
        'type': 'object',
        'additionalProperties': False
    }
}
```

```python
tools = [{"type": "function", "function": create_checklist_json},
        {"type": "function", "function": mark_complete_json}]
```

```python
def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        tool = globals().get(tool_name)
        result = tool(**arguments) if tool else {}
        results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
    return results
```

```python
def loop(messages):
    response = openai.chat.completions.create(model="gpt-5.5", messages=messages, tools=tools)
    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        tool_calls = message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(message)
        messages.extend(results)
        response = openai.chat.completions.create(model="gpt-5.5", messages=messages, tools=tools)
    show(response.choices[0].message.content)
```

```python
system_message = """
You are given a problem to solve, by using your checklist tools to plan a list of steps, then carrying out each step in turn.
Now create a plan, set the checklist, carry out the steps, and reply with the solution.
If any quantity isn't provided in the question, then include a step to come up with a reasonable estimate.
Provide your solution in Rich console markup without code blocks.
Do not ask the user questions or clarification; respond only with the answer after using your tools.
"""
user_message = """"
A train leaves Boston at 2:00 pm traveling 60 mph.
Another train leaves New York at 3:00 pm traveling 80 mph toward Boston.
When do they meet?
"""
messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_message}]
```

```python
checklist, completed = [], []
loop(messages)
```

<table style="margin: 0; text-align: left; width:100%">
    <tr>
        <td style="width: 150px; height: 150px; vertical-align: middle;">
            <img src="../assets/exercise.png" width="150" height="150" style="display: block;" />
        </td>
        <td>
            <h2 style="color:#ff7800;">Ćwiczenie</h2>
            <span style="color:#ff7800;">Teraz spróbuj sam zbudować Pętlę Agenta od zera!<br/>
            Stwórz nowy .ipynb i zrób ją od podstaw, wracając do tego w razie potrzeby.<br/>
            To jeden z niewielu przypadków, gdy polecam pisanie od zera - to bardzo satysfakcjonujący efekt.
            </span>
        </td>
    </tr>
</table>
