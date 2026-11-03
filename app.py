import json
import shutil
from pathlib import Path

save_file = Path("data/save.json")
sessions_file = Path("data/sessions.json")
setup_files_missing = not save_file.exists() or not sessions_file.exists()

save_file.parent.mkdir(parents=True, exist_ok=True)
if not save_file.exists():
    shutil.copyfile("data/save.json.example", save_file)
if not sessions_file.exists():
    shutil.copyfile("data/sessions.json.example", sessions_file)

from dotenv import load_dotenv
import openai
import utils, sys, communication, requests, os, time, datetime, local, setup
from utils import config as cnfg
from openai import OpenAI
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog, message_dialog
from prompt_toolkit.styles import Style
from config import LOCAL_MODELS_REGISTRY, availableModels, MENU_STYLE
import sessionhandle as sh

bootuptime = time.time()

os.system("cls" if os.name == "nt" else "clear")
print("Loading Epo Playground...")
utils.printlogo(printmesg=True)

print("Variables", end='... ')

chosenModel = cnfg.get('General', 'default_model')
chosenProvider = None

model_system_prompt = ""

try:

    with open("data/save.json", "r") as file:
        save = json.load(file)
    session = PromptSession()
    sh.startsession()
    
except Exception as error:
    raise Exception(f"FAIL\n{error}") from error

print("OK")
    
print("Functions", end='... ')

try:
    
    def cls():
        os.system("cls" if os.name == "nt" else "clear")
    def commcls():
        os.system("cls" if os.name == "nt" else "clear")
        utils.printlogo(True, f"\nUse /help for well... help.\n\n")
    def commexit():
        print("Bye!")
        raise SystemExit
    def commnew():
        sh.newsession()
        print("Started new session.")
    def commhelp():
        print("""Available commands:
        /help - help
        /clear - clear screen
        /exit - exit
        /new - start a new session
        /model - change model
        /menu - menu""")
    def get_model_choices():
        model_choices = []
        model_choice_map = {}
        enabled_providers = save.get("enabledProviders", [])
        for provider, provider_models in availableModels.items():
            if provider != "local" and provider not in enabled_providers:
                continue
            for model in provider_models:
                if model.startswith("local:"):
                    info = LOCAL_MODELS_REGISTRY.get(model, {})
                    label = f"{info.get('name', model)} (lokalny)"
                    choice = model
                else:
                    choice = f"{provider}|{model}"
                    label = f"{provider}:{model}"
                model_choices.append((choice, label))
                model_choice_map[choice] = (model, provider)
        return model_choices, model_choice_map
    def changemodel():
        global chosenModel, chosenProvider, model_system_prompt
        model_choices, model_choice_map = get_model_choices()
        if not model_choices:
            print("No models available. Enable a provider or add a local model.")
            return
        selection = radiolist_dialog(
            title="Model Selection",
            text=f"Current model: {chosenModel}\nChoose a model:",
            values=model_choices,
            style=MENU_STYLE
        ).run()
        if selection:
            chosenModel, chosenProvider = model_choice_map[selection]
            save["selectedModel"] = chosenModel
            setup.save["selectedModel"] = chosenModel
            if chosenModel.startswith("local:"):
                info = LOCAL_MODELS_REGISTRY.get(chosenModel, {})
                sp_path = info.get("system_prompt_path", "")
                if sp_path and Path(sp_path).exists():
                    with open(sp_path, 'r', encoding='utf-8') as f:
                        model_system_prompt = f.read()
                else:
                    model_system_prompt = ""
            else:
                model_system_prompt = ""
            local._update_system_prompt(model_system_prompt)
            print(f"Model changed to {chosenModel}")
            setup.dump_save()
        else:
            print("Model selection cancelled.")
    def commprovider():
        enabled_providers = set(save.get("enabledProviders", []))
        setup.addprovider()
        with open("data/save.json", "r") as file:
            updated_save = json.load(file)
        save.clear()
        save.update(updated_save)
        setup.save.clear()
        setup.save.update(updated_save)
        if set(save.get("enabledProviders", [])) - enabled_providers:
            changemodel()
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
                    local.setup_mosaic_v1()

except Exception as error:
    raise Exception(f"FAIL\n{error}") from error

print("OK")

if setup_files_missing or save.get("firstTime", True):
    print("First time using Epo Playground. Running setup...")
    setup.introduction()
    with open(save_file, "r") as file:
        updated_save = json.load(file)
    save.clear()
    save.update(updated_save)
    setup.save.clear()
    setup.save.update(updated_save)
    sh.startsession()


commands = {
        "/help": commhelp,
        "/clear": commcls,
        "/exit": commexit,
        "/new": commnew,
        "/model": changemodel,
        "/menu": commmenu,
        "/provider": commprovider,
}

local.scan_local_models()

model_choices, model_choice_map = get_model_choices()
selected_model = save.get("selectedModel", "")
selected_choice = next(
    (
        choice
        for choice, _ in model_choices
        if model_choice_map[choice][0] == selected_model
    ),
    None,
)
if selected_choice:
    chosenModel, chosenProvider = model_choice_map[selected_choice]
elif model_choices:
    chosenModel, chosenProvider = model_choice_map[model_choices[0][0]]
    save["selectedModel"] = chosenModel
    setup.save["selectedModel"] = chosenModel
    setup.dump_save()

completer = WordCompleter(list(commands.keys()), ignore_case=True, sentence=True)

cls()
utils.printlogo(True, f"\nUse /help for well... help.\n\n")

print(f"Current model: {chosenModel} (provider: {chosenProvider})")

while True:
    try:
        usr_prompt = session.prompt(">> ", completer=completer).strip()
        funkcja = commands.get(usr_prompt)

        if funkcja is not None:
            funkcja()
            continue

        start = time.time()
        communication.requestAPI(
            usr_prompt, chosenModel, availableModels, chosenProvider
        )
        end = time.time()
        sh.savesession()

        print(f"Finished in {end - start:.2f}s")
    except KeyboardInterrupt:
        print("\nBye!")
        break
    except openai.AuthenticationError:
        print("Authentication error. Check your API key. It can be expired or invalid. ")