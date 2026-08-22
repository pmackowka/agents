# Async Python

## Briefing o asynchronicznym programowaniu w Pythonie, kluczowym w inżynierii agentów

Oto mistrzowski samouczek od wiadomo-kogo, z ćwiczeniami i porównaniami.

https://chatgpt.com/share/680648b1-b0a0-8012-8449-4f90b540886c

Obejmuje to, jak uruchamiać kod async z modułu Pythona.

### A teraz kilka przykładów:

```python
# Let's define an async function

import asyncio

async def do_some_work():
    print("Starting work")
    await asyncio.sleep(1)
    print("Work complete")
```

```python
# What will this do?

do_some_work()
```

```python
# OK let's try that again!

await do_some_work()
```

```python
# What's wrong with this?

async def do_a_lot_of_work():
    do_some_work()
    do_some_work()
    do_some_work()

await do_a_lot_of_work()
```

```python
# Interesting warning! Let's fix it

async def do_a_lot_of_work():
    await do_some_work()
    await do_some_work()
    await do_some_work()

await do_a_lot_of_work()
```

```python
# And now let's do it in parallel
# It's important to recognize that this is not "multi-threading" in the way that you may be used to
# The asyncio library is running on a single thread, but it's using a loop to switch between tasks while one is waiting

async def do_a_lot_of_work_in_parallel():
    await asyncio.gather(do_some_work(), do_some_work(), do_some_work())

await do_a_lot_of_work_in_parallel()
```

### Na koniec - spróbuj napisać moduł Pythona, który wywołuje do_a_lot_of_work_in_parallel

Zobacz link na górze; będziesz potrzebować w swoim module czegoś takiego:

```python
if __name__ == "__main__":
    asyncio.run(do_a_lot_of_work_in_parallel())
```
