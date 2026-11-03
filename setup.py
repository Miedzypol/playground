import utils, os, json, shutil
from config import MENU_STYLE
from rich.console import Console
from rich.panel import Panel
console = Console()

with open("data/save.json", "r") as file:
    save = json.load(file)

from prompt_toolkit.shortcuts import radiolist_dialog 

def dump_save():
    with open("data/save.json", "w") as file:
        json.dump(save, file)

# console.print(Panel("content",title="title",border_style="green",))

def addprovider(): 
    providers = [
        ("openrouter", "OpenRouter (RECOMMENDED)"),
        ("groq", "Groq"),
    ]
    available_providers = [
        provider for provider in providers
        if provider[0] not in save['enabledProviders']
    ]
    if not available_providers:
        print("All providers are already enabled.")
        return

    choice = radiolist_dialog(
        title="Provider Selection",
        text="Select the provider you'll like to use.",
        values=available_providers,
        style=MENU_STYLE,
        ok_text="Select",
    ).run()
    if choice == 'openrouter':
        print("Remembered. Put your OpenRouter API key in the .env file.")
        save['enabledProviders'].append('openrouter')
    elif choice == 'groq':
        print("Remembered. Put your Groq API key in the .env file.")
        save['enabledProviders'].append('groq')
    dump_save()
    

def introduction():
    print('setup.py booted')
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Panel("Wait, we are currently initializing your environment.",title="Initializing...",border_style="red",))
    shutil.copyfile('data/save.json.example', 'data/save.json')
    shutil.copyfile('data/sessions.json.example', 'data/sessions.json')
    console.print(Panel("Welcome to the Playground! Let's get started. Press enter to continue.",title="",border_style="green",))
    input()
    console.print(Panel("To get you started, you need to select a provider. Do you want to do it now?",title="Providers",border_style="green",))
    option = input("Y/N: ").strip().lower()

    if option=='y':addprovider()

    print(f"\nIf you want to add another provider later, use /provider command in the app.")
    input(f"\n\nPress enter to continue...")
    os.system("cls" if os.name == "nt" else "clear")
    console.print(Panel("Hello, u-uhh... what was your username?",title="User Information",border_style="green",))
    save['username'] = input("Username: ")

    console.print(Panel(f"All set up, {save['username']}! Welcome to the Playground!",title="Welcome!",border_style="green",))
    save['firstTime'] = False
    input(f"\n\nPress enter to continue...")
    dump_save()

