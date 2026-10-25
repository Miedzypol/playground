import os, time, datetime, requests
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

os.system("cls" if os.name == "nt" else "clear")
print("Inicjalizacja Epo Playground...")

print("Zmienne", end='... ')

chosenModel = "inception/mercury-2.5"

try:
    version = '1.0'

    systemPrompt = f"""You are Mistral Nemo, a helper AI in the Epo Playground app.
    Respond to user in a nice, polite way, listen to it. You cannot commit anything illegal.
    Do not use emojis and emojis in this format: :smile:, :sad: :drool:, you can use ASCII to make them (example: :D, :P, :3, :), :(), etc.). D
    If user meows, meow to him back.

    Basic information:
    - Epo Playground is made by Project Aurly
    - Current date and time: {datetime.datetime.now()}

    Your tools:
    - Basic Markdown support, example: *italic* **bold** ***italic and bold***.

    User prompt:
    """
    load_dotenv() 
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )
    
    

    session = PromptSession()
    messages = [{"role": "system", "content": systemPrompt}]
except Exception as error:
    raise Exception(f"FAIL\n{error}") from error

print("OK")


print("OpenRouter", end='... ')

url = "https://openrouter.ai/"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    if response.status_code != 200:
        print(f"FAIL\n response: {response.status_code}\nPossible causation of the error:\n- Not connected to the internet\n- OpenRouter is down\n\nIf not then idk")
        raise SystemExit

finally:
    print("OK")
"""except requests.RequestException as error:
    print(f"FAIL: {error}")"""
    


print("Functions", end='... ')

try:
    def requestAPI(prompt, boolStream):
        messages.append({"role": "user", "content": prompt})
        stream = client.chat.completions.create(
        model=chosenModel,
        messages=messages,
        stream=True,
        )
        full = ""
        print("\nAI: ", end="", flush=True)
        is_first = True
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                text = text.replace("\\n", "\n")
                if is_first:
                    text = text.lstrip("\n")
                    is_first = False
                print(text, end="", flush=True)
                full += text
        print()
        messages.append({"role": "assistant", "content": full})
    def cls():
        os.system("cls" if os.name == "nt" else "clear")
    def commcls():
        os.system("cls" if os.name == "nt" else "clear")
        print(f'Epo Playground v{version}\nUse /help for well... help.\n\n')
    def commexit():
        print("Bye!")
        raise SystemExit
    def commnew():
        messages.clear()
        messages.append({"role": "system", "content": systemPrompt})
        print("Started new session.")
    def commhelp():
        print("""Aviable commands:
        /help - help
        /clear - clear screen
        /exit - exit
        /new - start a new session""")
except Exception as error:
    raise Exception(f"FAIL\n{error}") from error

print("OK")

komendy = {
        "/help": commhelp,
        "/clear": commcls,
        "/exit": commexit,
        "/new": commnew,
}

completer = WordCompleter(list(komendy.keys()), ignore_case=True)

cls()
print(f'Epo Playground v{version}\nUse /help for well... help.\n\n')

while True:
    usr_prompt = session.prompt(">> ", completer=completer).strip()
    funkcja = komendy.get(usr_prompt)

    if funkcja is not None:
        funkcja()
        continue

    start = time.time()
    requestAPI(usr_prompt, True)
    end = time.time()

    print(f"Finished in {end - start:.2f}s")