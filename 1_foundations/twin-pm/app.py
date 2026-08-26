from anthropic import Anthropic  # klient Anthropic zamiast OpenAI
from context import TWIN_SYSTEM_PROMPT  # gotowy prompt systemowy zbudowany w context.py
from tools import tools, handle_tool_calls  # definicje narzędzi i funkcja obsługująca ich wywołania
from styles import CSS, JS, EXAMPLES  # style, skrypt JS i przykładowe pytania do UI Gradio
from dotenv import load_dotenv  # wczytywanie zmiennych z pliku .env
import gradio as gr  # framework UI czatu

load_dotenv(override=True)  # wczytuje .env i nadpisuje już ustawione zmienne środowiskowe

MODEL_NAME = "claude-haiku-4-5"  # najtańszy model Anthropic - pułap kosztowy na czas kursu

anthropic = Anthropic()  # klient automatycznie odczyta klucz z ANTHROPIC_API_KEY w .env

system_prompt = TWIN_SYSTEM_PROMPT  # trzymany osobno jako string, bo Anthropic przyjmuje system jako parametr top-level, nie wpis w messages


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]  # Gradio może dawać dodatkowe klucze w historii (np. metadata) - Anthropic akceptuje tylko role/content
    messages = history + [{"role": "user", "content": message}]  # bez wpisu "system" na liście - trafia osobno do system=
    response = anthropic.messages.create(model=MODEL_NAME, max_tokens=16000, system=system_prompt, tools=tools, messages=messages)  # max_tokens wymagany przez Anthropic, system_prompt jako top-level parametr
    while response.stop_reason == "tool_use":  # pętla trwa, dopóki Claude chce użyć narzędzia (stop_reason, nie finish_reason jak w OpenAI)
        tool_calls = [block for block in response.content if block.type == "tool_use"]  # wyciągnij wszystkie bloki tool_use z odpowiedzi
        results = handle_tool_calls(tool_calls)  # tools.py zwraca gotową listę bloków tool_result
        messages.append({"role": "assistant", "content": response.content})  # cała odpowiedź assistant (razem z blokiem tool_use) wraca do historii
        messages.append({"role": "user", "content": results})  # wszystkie wyniki narzędzi w JEDNEJ wiadomości user - Claude oczekuje ich razem, nie po jednej na wiadomość
        response = anthropic.messages.create(model=MODEL_NAME, max_tokens=16000, system=system_prompt, tools=tools, messages=messages)  # kolejne zapytanie z dołączonymi wynikami narzędzi
    return next(block.text for block in response.content if block.type == "text")  # odporne na ThinkingBlock, w przeciwieństwie do response.content[0].text


if __name__ == "__main__":  # uruchom serwer Gradio tylko przy bezpośrednim odpaleniu pliku, nie przy imporcie
    gr.ChatInterface(  # buduje UI czatu wokół funkcji chat()
        chat,  # funkcja wywoływana przy każdej wiadomości użytkownika
        examples=EXAMPLES,  # przykładowe pytania pokazywane pod czatem
        title="Cyfrowy Bliźniak",  # nagłówek H1 nad czatem
        description="Porozmawiaj z moim cyfrowym bliźniakiem o mojej karierze",  # podtytuł pod nagłówkiem
        chatbot=gr.Chatbot(show_label=False),  # ukrywa domyślną etykietę komponentu Chatbot
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())  # odpala lokalny serwer, wstrzykuje własny CSS/JS i bazowy motyw Gradio
