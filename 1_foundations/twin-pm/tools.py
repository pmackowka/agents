import json  # do (de)serializacji argumentów i wyników narzędzi
import os  # do odczytu zmiennych środowiskowych (klucze Pushover)
import requests  # do wysyłania powiadomień push przez HTTP
from dotenv import load_dotenv  # wczytywanie zmiennych z pliku .env

load_dotenv(override=True)  # wczytuje .env i nadpisuje już ustawione zmienne środowiskowe

pushover_user = os.getenv("PUSHOVER_USER")  # klucz użytkownika Pushover z .env
pushover_token = os.getenv("PUSHOVER_TOKEN")  # klucz aplikacji Pushover z .env

pushover_url = "https://api.pushover.net/1/messages.json"  # endpoint API Pushover do wysyłki powiadomień


def push(text):  # wysyła powiadomienie push na telefon
    requests.post(  # wysyła zapytanie POST do API Pushover
        pushover_url,  # adres endpointu
        data={  # dane formularza wymagane przez Pushover
            "token": pushover_token,  # identyfikuje aplikację Pushover
            "user": pushover_user,  # identyfikuje odbiorcę powiadomienia
            "message": text,  # treść powiadomienia
        },
    )


def record_user_details(email, name="Imię nie podane", notes="brak"):  # narzędzie wywoływane przez Claude, gdy użytkownik chce zostawić kontakt - defaulty widoczne w puszu, jeśli Claude ich nie poda
    push(f"Zapisano zainteresowanie od {name}, email {email}, notatki: {notes}")  # treść powiadomienia push - to Piotr czyta na telefonie, więc po polsku
    return "Zapisano"  # zwracany tekst trafia do tool_result i wraca do Claude


def record_unknown_question(question):  # narzędzie wywoływane przez Claude, gdy nie zna odpowiedzi
    push(f"Zapisano pytanie bez odpowiedzi: {question}")  # treść powiadomienia push - to Piotr czyta na telefonie, więc po polsku
    return "Zapisano"  # zwracany tekst trafia do tool_result i wraca do Claude


record_user_details_json = {  # definicja narzędzia record_user_details w formacie Anthropic
    "name": "record_user_details",  # nazwa narzędzia - Claude widzi ją i decyduje, kiedy je wywołać
    "description": "Użyj tego narzędzia, żeby zapisać, że użytkownik jest zainteresowany kontaktem i podał adres email",  # opis czytany przez model przy decyzji o wywołaniu
    "input_schema": {  # Anthropic używa klucza input_schema, nie parameters jak OpenAI
        "type": "object",  # JSON Schema, ten sam format co w OpenAI
        "properties": {  # definicje poszczególnych pól argumentów
            "email": {"type": "string", "description": "Adres email tego użytkownika"},  # jedyne pole wymagane (patrz required niżej)
            "name": {"type": "string", "description": "Imię użytkownika, jeśli je podał"},  # opcjonalne - ma domyślną wartość w record_user_details()
            "notes": {
                "type": "string",  # typ pola w JSON Schema
                "description": "Dodatkowe informacje o rozmowie, warte zapisania jako kontekst",  # opis pola czytany przez model
            },  # opcjonalne, jak name
        },
        "required": ["email"],  # tylko email jest wymagany - reszta ma defaulty w sygnaturze funkcji
        "additionalProperties": False,  # Claude nie może dosłać pól spoza schematu
    },
}

record_unknown_question_json = {  # definicja narzędzia record_unknown_question w formacie Anthropic
    "name": "record_unknown_question",  # nazwa narzędzia widoczna dla modelu
    "description": "Zawsze użyj tego narzędzia, żeby zapisać każde pytanie, na które nie potrafiłeś odpowiedzieć, bo nie znałeś odpowiedzi",  # instrukcja dla modelu, kiedy wywołać narzędzie
    "input_schema": {  # jak wyżej: input_schema, nie parameters
        "type": "object",  # JSON Schema
        "properties": {  # definicja jedynego pola argumentu
            "question": {"type": "string", "description": "Pytanie, na które nie udało się odpowiedzieć"},  # jedyne pole, zawsze wymagane
        },
        "required": ["question"],  # bez tego pola narzędzie nie ma sensu
        "additionalProperties": False,  # Claude nie może dosłać pól spoza schematu
    },
}

tools = [record_user_details_json, record_unknown_question_json]  # Anthropic przyjmuje płaską listę definicji narzędzi, bez opakowania {"type": "function", "function": ...} jak w OpenAI

tool_map = {  # mapowanie nazwy narzędzia (jak w tools) na faktyczną funkcję Pythona do wywołania
    "record_user_details": record_user_details,  # nazwa musi się zgadzać z "name" w record_user_details_json
    "record_unknown_question": record_unknown_question,  # nazwa musi się zgadzać z "name" w record_unknown_question_json
}


def handle_tool_calls(tool_calls):  # przetwarza wszystkie bloki tool_use z jednej odpowiedzi Claude
    results = []  # tu zbieramy bloki tool_result do jednej wspólnej wiadomości user
    for tool_call in tool_calls:  # tool_calls to lista bloków tool_use wyciągnięta z response.content w app.py
        tool_name = tool_call.name  # blok tool_use ma name bezpośrednio, nie zagnieżdżone w .function jak w OpenAI
        arguments = tool_call.input  # input jest już sparsowanym dict, nie JSON-stringiem jak tool_call.function.arguments w OpenAI
        print(f"Tool called: {tool_name}", flush=True)  # log do konsoli, bez zmian względem OpenAI
        tool = tool_map.get(tool_name)  # znajdź właściwą funkcję Pythona po nazwie narzędzia
        result = tool(**arguments) if tool else "Nieznane narzędzie: " + tool_name  # wywołaj funkcję z rozpakowanymi argumentami - tekst błędu też trafia do Claude jako tool_result
        results.append({  # dokłada blok tool_result do listy wyników
            "type": "tool_result",  # Anthropic identyfikuje wynik po type, nie po roli "tool" jak w OpenAI
            "tool_use_id": tool_call.id,  # musi się zgadzać z id bloku tool_use, żeby Claude powiązał wynik z wywołaniem
            "content": json.dumps(result),  # treść wyniku zserializowana do JSON-a
        })
    return results  # lista bloków tool_result - app.py opakuje ją w jedną wiadomość user
