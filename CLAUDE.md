# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Co to jest

Materiały kursu "Master AI Agentic Engineering" Eda Donnera — 6 tygodni labów budujących autonomiczne agenty. Nie jest to aplikacja produkcyjna: każdy folder tygodnia to osobny, samodzielny projekt dydaktyczny.

## Środowisko i komendy

Menedżer pakietów to `uv`, Python przypięty na 3.12.12. Nie edytuj ręcznie `uv.lock`.

```bash
uv sync                      # instalacja zależności (uv run robi to samo w tle)
uv run app.py                # uruchomienie skryptu — NIE python app.py
uv add <pakiet>              # dodanie zależności do pyproject.toml
```

Notebooki uruchamia się w Cursorze/VS Code z kernelem `.venv (Python 3.12.x)` z katalogu głównego projektu.

Aplikacje Gradio (`uv run app.py` z katalogu danego tygodnia):
- `1_foundations/twin-pm/app.py` — cyfrowy bliźniak
- `2_openai/deep_research/app.py` — deep research
- `4_langchain_langgraph/app.py` — Sidekick
- `6_mcp/app.py` — dashboard trading floor

Node (tygodnie 4, 5, 6) — wymagany v22+, po instalacji restart Cursora, nie tylko kernela:
```bash
cd 5_agent_frameworks/4_mastra && npm install && npm run step1   # ... step5, worker
cd 6_mcp/frontend && npm install && npm run dev                  # alternatywny frontend do Gradio
```

Docker jest wymagany tylko dla crew `coder` i `engineering_team` (tydzień 3) — uruchamiają wygenerowany kod w kontenerze.

Brak CI, brak pakietowego runnera testów. Pojedyncze `test_*.py` w `3_crewai/reference/engineering_team/sandbox_*/` to artefakty wygenerowane przez agentów, nie testy repo.

## Architektura — rzeczy nieoczywiste

### Tydzień 3 to osobne projekty uv
`3_crewai/reference/*` i `3_crewai/coursework/*` mają **własne** `pyproject.toml` i `uv.lock` — nie korzystają z roota. CrewAI instaluje się jako narzędzie globalne, przypięte do wersji z kursu:
```bash
uv tool install crewai==1.14.4
cd 3_crewai/reference/debate && crewai run
crewai create crew <nazwa>   # z katalogu 3_crewai
```
Struktura crew: `src/<nazwa>/config/{agents,tasks}.yaml` (prompty deklaratywnie w YAML) + `crew.py` + `main.py`. Każdy crew ma auto-generowany `AGENTS.md` od CrewAI, który każe weryfikować API względem żywej dokumentacji zamiast pamięci modelu — CrewAI robi breaking changes.

### Tydzień 5: wzorzec board + worker
Sedno tygodnia 5: **ten sam worker napisany pięć razy w pięciu frameworkach** (Strands, Pydantic AI, Microsoft Agent Framework, Agno, Mastra/TS); Google ADK gra rolę orkiestratora, nie workera. Wspólnym podłożem jest `board.py` — mikro-todo-lista na SQLite (WAL + busy timeout, żeby kilka agentów pisało równolegle). Plik jest **skopiowany identycznie** do folderu każdego dnia; edycja jednej kopii nie propaguje się na resztę.

Workery są dwutrybowe, sterowane `sys.argv`:
```bash
uv run pydantic_worker.py                       # tryb standalone (demo danego dnia)
uv run pydantic_worker.py <taskId> <boardPath>  # dzień 5: jedno zadanie na wspólnej tablicy
```
`BOARD_PATH` musi trafić do env **przed** importem `board` (board czyta ścieżkę przy imporcie) — stąd nietypowa kolejność importów z `# noqa: E402` w workerach.

Dzień 5 (`5_agent_loop/`) to orkiestrator ADK, który odpala te same, niezmienione workery z dni 2-4 jako podprocesy przeciw jednej wspólnej tablicy, a QA-agent sprawdza wynik w prawdziwym Chrome przez Playwright MCP. Workery są wykrywane po istnieniu pliku (`catalog.py`) — brakujący plik po prostu wypada z zespołu, bez błędu.

### Tydzień 6: trading floor
`6_mcp/backend/` to serwery MCP uruchamiane jako podprocesy przez stdio (`uv run -m backend.accounts_server` itd.), spinane w `mcp_servers.py`. Konfiguracja przez zmienne środowiskowe: `RUN_EVERY_N_MINUTES`, `RUN_EVEN_WHEN_MARKET_IS_CLOSED`, `USE_MANY_MODELS`. Bez klucza `MASSIVE_API_KEY` market data leci z lokalnego symulatora (`market_server`) — kod sam wybiera wariant. Dwa frontendy nad tym samym backendem: Gradio (`app.py` + `demo/`) i osobny Vite/TS (`frontend/`, konsumuje JSON z `backend/api.py`).

### Tydzień 4: Sidekick
`sidekick.py` — pojedynczy `create_agent` opakowany własną pętlą ewaluatora (max 3 podejścia), z middleware: TodoList (plan współdzielony z UI), PII, ModelCallLimit, HumanInTheLoop. Agent pisze wyłącznie do `4_langchain_langgraph/sandbox/` (gitignorowany poza `skills/`).

### Podmiana modelu
Każdy dzień tygodnia 5 ma `SWAP_AI.md` z gotowym przepisem na innego dostawcę dla swojego frameworka. Wzorzec w całym repo: model czytany z env ze stałym fallbackiem, np. `WORKER_MODEL`, `ORCHESTRATOR_MODEL` — nadpisuj per-run zamiast edytować plik. Ogólne przepisy (Gemini, DeepSeek, Ollama, OpenRouter, Azure) są w `guides/09_ai_apis_and_ollama.ipynb`.

### Klucze i sekrety
Jeden `.env` w katalogu głównym repo, wczytywany wszędzie przez `load_dotenv(override=True)`. `.cursorignore` zawiera tylko `.env`. Wymagany minimalnie `OPENAI_API_KEY`; opcjonalnie `GOOGLE_API_KEY`/`GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `TAVILY_API_KEY`, `MASSIVE_API_KEY`, Pushover, SMTP.

## Git remotes i plan PR-a do instruktora

Repo powstało jako `gh repo create --source=.` z historią `ed-donner/agents`, **nie** jako GitHub Fork — `gh api repos/pmackowka/Agents --jq .fork` zwraca `false`. To ma konsekwencje dla wysyłki PR-a.

- `origin` → `pmackowka/Agents` (prywatne). Codzienna praca, commity, push — bez ograniczeń, pełny zapis.
- `upstream` → `ed-donner/agents` (publiczne, instruktora). Tylko odbiór: `git fetch upstream && git merge upstream/main`. Brak prawa zapisu, nie próbuj tam pushować.
- Wielkość liter w nazwie repo (`Agents` vs `agents`) nie ma znaczenia — GitHub jest case-insensitive dla URL-i repo.

**Cel końcowy kursu wymaga wysłania PR-a do `ed-donner/agents`** (zaliczenie/certyfikat). Ponieważ `origin` nie jest zarejestrowanym forkiem, GitHub nie pozwoli otworzyć PR-a bezpośrednio z niego — trzeba dopiero w tym celu:
1. `gh repo fork ed-donner/agents --remote=true --remote-name=pr-fork` — tworzy prawdziwy, **publiczny** fork (GitHub nie oferuje prywatnych forków publicznych repo poza Enterprise) i dodaje go jako trzeci remote.
2. Push brancha z rozwiązaniem (docelowo tylko zmiany w `community_contributions/`, zgodnie z regułami PR w `guides/03_git_and_github.ipynb`) na `pr-fork`.
3. `gh pr create --repo ed-donner/agents`.
4. Remote `pr-fork` można potem usunąć, żeby wrócić do układu 2-remote'owego.

Nie zakładaj tego trzeciego remote'a przy zwykłej pracy — tylko w momencie faktycznej wysyłki PR-a.

## Konwencje repo

- `community_contributions/` w każdym tygodniu — tam trafiają prace kursantów. Kod kursu tam nie mieszka; przy szukaniu wzorców referencyjnych ten katalog zwykle pomijaj.
- `guides/` (12 notebooków) i `1_foundations/` (laby 1-5) mają polskie kopie `NN_nazwa.pl.ipynb` / `N_lab.pl.ipynb` — pełne notatniki, nie osobne pliki markdown (wcześniejsze `.pl.md` zostały usunięte i zastąpione). Tłumaczone jest wszystko: markdown, komentarze w kodzie i stringi-prompty przekazywane do modelu; sama składnia kodu (nazwy zmiennych, wywołania API) zostaje bez zmian. Zmieniając oryginalny notebook, zaktualizuj też odpowiednik `.pl.ipynb`.
- Osobiste kopie `1_foundations/*.pl.ipynb` bywają dodatkowo przerobione z OpenAI SDK na natywne SDK Anthropic — Piotr używa Claude, nie OpenAI, do własnej pracy nad kursem. Do tej podmiany służy project-scoped skill `.claude/skills/swap/`, do dopisywania przykładowych rozwiązań ćwiczeń w tych labach — skill `.claude/skills/solve/`. Nie myl tych plików z materiałem referencyjnym: oryginalne `.ipynb` (bez `.pl`) to niezmieniony kod instruktora na OpenAI i taki ma zostać.
- Do wypuszczenia PR-a na upstream obowiązują reguły z `guides/03_git_and_github.ipynb`: zmiany wyłącznie w `community_contributions`, wyczyszczone outputy notebooków, <2000 linii.
