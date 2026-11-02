import os, time, datetime
from utils import config
import requests
from openai import OpenAI
from dotenv import load_dotenv
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog, message_dialog
from prompt_toolkit.styles import Style
import utils
import sys
import shutil
from pathlib import Path

os.system("cls" if os.name == "nt" else "clear")
print("Inicjalizacja Epo Playground...")
utils.printlogo(printmesg=True)

print("Zmienne", end='... ')

chosenModel = config.get('General', 'default_model')
availableModels = [
    "recursive/flint-v1.0:free",
    "poolside/laguna-s-2.1:free",
    "mistralai/mistral-nemo",
    "inclusionai/ling-3.0-flash",
    "openai/gpt-oss-120b",
]

APP_DIR = Path(__file__).resolve().parent
LOCAL_MODELS_DIR = APP_DIR / "models"
LOCAL_MODELS_REGISTRY = {}
model_system_prompt = ""

MENU_STYLE = Style.from_dict({
    'dialog': 'bg:#728E6D',
    'dialog.title': 'bg:#728E6D #E5CD82 bold',
    'dialog.body': 'bg:#728E6D #ffffff',
    'button': 'bg:#E5CD82 #000000',
    'button.focused': 'bg:#FFF2B4 #000000',
    'radio-list': 'bg:#728E6D #ffffff',
    'radio-list.selected': 'bg:#FFF2B4 #000000',
})


try:

    _base_system_prompt = f"""You are Mistral Nemo, a helper AI in the Epo Playground app.
    Respond to user in a nice, polite way, listen to it. You cannot commit anything illegal.
    Do not use emojis and emojis in this format: :smile:, :sad: :drool:.
    If user meows, meow to him back.

    Basic information:
    - Epo Playground is made by Project Aurly
    - Current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Your tools:
    - Basic Markdown support, example: *italic* **bold** ***italic and bold***.

    User prompt:
    """
    systemPrompt = _base_system_prompt
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
        if chosenModel.startswith("local:"):
            model_info = LOCAL_MODELS_REGISTRY.get(chosenModel)
            if not model_info:
                print(f"\nNie znaleziono modelu lokalnego: {chosenModel}")
                return
            try:
                from llama_cpp import Llama
            except ImportError:
                print("\nDo uzycia modeli lokalnych wymagana jest biblioteka llama-cpp-python.")
                print("Zainstaluj: pip install llama-cpp-python")
                return
            print("\nInicjalizacja modelu lokalnego (moze zajac chwile)...")
            messages.append({"role": "user", "content": prompt})
            try:
                llm = Llama(model_path=model_info["path"], n_ctx=2048, verbose=False)
            except Exception as e:
                print(f"\nBlad ladowania modelu: {e}")
                print("Sprawdz czy plik modelu jest prawidlowy i czy biblioteka llama-cpp-python jest aktualna.")
                return
            prompt_text = f"{systemPrompt}\n\nUser: {prompt}\nAssistant:"
            full = ""
            print("\nAI: ", end="", flush=True)
            is_first = True
            for chunk in llm(prompt_text, max_tokens=512, stop=["\n\nUser:", "\n\nAssistant:"], stream=True):
                text = chunk["choices"][0]["text"]
                if text:
                    if is_first:
                        text = text.lstrip("\n")
                        is_first = False
                    print(text, end="", flush=True)
                    full += text
            print()
            messages.append({"role": "assistant", "content": full})
        else:
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
        utils.printlogo(True, f"\nUse /help for well... help.\n\n")
    def commexit():
        print("Bye!")
        raise SystemExit
    def commnew():
        messages.clear()
        messages.append({"role": "system", "content": systemPrompt})
        print("Started new session.")
    def commhelp():
        print("""Available commands:
        /help - help
        /clear - clear screen
        /exit - exit
        /new - start a new session
        /model - change model
        /menu - menu""")
    def changemodel():
        global chosenModel, model_system_prompt
        model_choices = []
        for m in availableModels:
            if m.startswith("local:"):
                info = LOCAL_MODELS_REGISTRY.get(m, {})
                label = info.get("name", m)
                model_choices.append((m, f"{label} (lokalny)"))
            else:
                model_choices.append((m, m))
        selection = radiolist_dialog(
            title="Model Selection",
            text=f"Current model: {chosenModel}\nChoose a model:",
            values=model_choices,
            style=MENU_STYLE
        ).run()
        if selection:
            chosenModel = selection
            if selection.startswith("local:"):
                info = LOCAL_MODELS_REGISTRY.get(selection, {})
                sp_path = info.get("system_prompt_path", "")
                if sp_path and Path(sp_path).exists():
                    with open(sp_path, 'r', encoding='utf-8') as f:
                        model_system_prompt = f.read()
                else:
                    model_system_prompt = ""
            else:
                model_system_prompt = ""
            _update_system_prompt()
            print(f"Model changed to {chosenModel}")
        else:
            print("Model selection cancelled.")

    def download_with_progress(url, dest, label="Pobieranie"):
        dest_path = Path(dest)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            resp = requests.get(url, stream=True, timeout=30)
            resp.raise_for_status()
        except Exception as e:
            print(f"\nBlad pobierania: {e}")
            return False
        total = int(resp.headers.get('content-length', 0))
        downloaded = 0
        start = time.time()
        with open(dest_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    downloaded += len(chunk)
                    f.write(chunk)
                    if total:
                        elapsed = time.time() - start
                        speed = downloaded / elapsed / 1024 if elapsed > 0 else 0
                        pct = downloaded / total * 100
                        bar_len = 25
                        filled = int(bar_len * downloaded / total)
                        bar = '█' * filled + '░' * (bar_len - filled)
                        print(f"\r{label} [{bar}] {pct:.1f}% ({speed:.0f} KB/s)", end='', flush=True)
        print(f"\r{label} ukonczone!{' ' * 40}")
        return True

    def _update_system_prompt():
        global systemPrompt
        if model_system_prompt:
            systemPrompt = f"{_base_system_prompt}\n\nModel-Specific Instructions:\n{model_system_prompt}"
        else:
            systemPrompt = _base_system_prompt
        if messages and messages[0]["role"] == "system":
            messages[0]["content"] = systemPrompt

    def setup_mosaic_v1():
        global chosenModel, model_system_prompt
        model_id = "local:mosaic-v1-quickfix"
        model_dir = APP_DIR / "models" / "mosaic" / "v1"
        model_path = model_dir / "mosaic-v1-quickfix.gguf"
        sys_prompt_path = model_dir / "system-prompt.md"
        print("\nModel: Mosaic v1 - QuickFix-2B")
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"Model juz pobrany ({size_mb:.0f} MB).")
        else:
            print("Rozpoczynanie pobierania...")
            url = "https://aurly.org/playground/models/mosaic/v1/mosaic-v1-quickfix.gguf"
            success = download_with_progress(url, model_path, "Pobieranie modelu")
            if not success:
                return
        sys_prompt_text = ""
        if sys_prompt_path.exists():
            with open(sys_prompt_path, 'r', encoding='utf-8') as f:
                sys_prompt_text = f.read()
        else:
            choice = radiolist_dialog(
                title="System Prompt",
                text="Do you want to download default system prompt?",
                values=[("yes", "Yes"), ("no", "No")],
                style=MENU_STYLE,
                ok_text="OK",
                cancel_text="Cancel",
            ).run()
            if choice == "yes":
                print("\nPobieranie system prompt...")
                sp_url = "https://aurly.org/playground/models/mosaic/v1/mosaic-v1-quickfix-systemprompt.md"
                if download_with_progress(sp_url, sys_prompt_path, "Pobieranie promptu"):
                    with open(sys_prompt_path, 'r', encoding='utf-8') as f:
                        sys_prompt_text = f.read()
        if sys_prompt_text:
            model_system_prompt = sys_prompt_text
        else:
            model_system_prompt = ""
        LOCAL_MODELS_REGISTRY[model_id] = {
            "name": "Mosaic v1 - QuickFix-2B",
            "path": str(model_path),
            "system_prompt_path": str(sys_prompt_path) if sys_prompt_text else "",
            "series": "Mosaic v1",
        }
        local_entry = model_id
        if local_entry not in availableModels:
            availableModels.append(local_entry)
        chosenModel = local_entry
        _update_system_prompt()
        print(f"\nPrzelaczono na model: Mosaic v1 - QuickFix-2B (lokalny)")
        print("Uzyj /new aby rozpoczac nowa sesje z tym modelem.")

    def scan_local_models():
        if not LOCAL_MODELS_DIR.exists():
            return
        for gguf_path in LOCAL_MODELS_DIR.rglob("*.gguf"):
            rel = gguf_path.relative_to(LOCAL_MODELS_DIR)
            stem = str(rel.with_suffix(''))
            model_id = f"local:{stem}"
            sp_path = gguf_path.parent / "system-prompt.md"
            sp = str(sp_path) if sp_path.exists() else ""
            LOCAL_MODELS_REGISTRY[model_id] = {
                "name": f"{rel.parent.name} - {rel.stem}",
                "path": str(gguf_path),
                "system_prompt_path": sp,
                "series": rel.parent.name,
            }
            if model_id not in availableModels:
                availableModels.append(model_id)

    def commmenu():
        choice = radiolist_dialog(
            title="Menu",
            text="Wybierz opcje:",
            values=[
                ("return", "Powrot"),
                ("test_local", "Przetestuj lokalnie modele Epo..."),
            ],
            style=MENU_STYLE,
            ok_text="Wybierz",
            cancel_text="Anuluj",
        ).run()
        if choice is None or choice == "return":
            return
        if choice == "test_local":
            series = radiolist_dialog(
                title="Wybor serii modeli",
                text="Ktora serie modeli chcesz przetestowac?",
                values=[("mosaic_v1", "Mosaic v1")],
                style=MENU_STYLE,
                ok_text="Wybierz",
                cancel_text="Anuluj",
            ).run()
            if series is None:
                return
            if series == "mosaic_v1":
                setup_mosaic_v1()

except Exception as error:
    raise Exception(f"FAIL\n{error}") from error

print("OK")




komendy = {
        "/help": commhelp,
        "/clear": commcls,
        "/exit": commexit,
        "/new": commnew,
        "/model": changemodel,
        "/menu": commmenu,
}

scan_local_models()

completer = WordCompleter(list(komendy.keys()), ignore_case=True)

cls()
utils.printlogo(True, f"\nUse /help for well... help.\n\n")

while True:
    try:
        usr_prompt = session.prompt(">> ", completer=completer).strip()
        funkcja = komendy.get(usr_prompt)

        if funkcja is not None:
            funkcja()
            continue

        start = time.time()
        requestAPI(usr_prompt, True)
        end = time.time()

        print(f"Finished in {end - start:.2f}s")
    except KeyboardInterrupt:
        print("\nBye!")
        break