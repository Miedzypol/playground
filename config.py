from pathlib import Path
import datetime, json, os
from dotenv import load_dotenv
from openai import OpenAI
from prompt_toolkit.styles import Style
APP_DIR = Path(__file__).resolve().parent
LOCAL_MODELS_DIR = APP_DIR / "models"
LOCAL_MODELS_REGISTRY = {}

# list(availableModels.keys())

MENU_STYLE = Style.from_dict({
    'dialog': 'bg:#728E6D',
    'dialog.title': 'bg:#728E6D #E5CD82 bold',
    'dialog.body': 'bg:#728E6D #ffffff',
    'button': 'bg:#E5CD82 #000000',
    'button.focused': 'bg:#FFF2B4 #000000',
    'radio-list': 'bg:#728E6D #ffffff',
    'radio-list.selected': 'bg:#FFF2B4 #000000',
})

with open("data/save.json", "r") as file:
    save = json.load(file)

load_dotenv() 
    
client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
)

availableModels = {
    "openrouter": [
        "mistralai/mistral-nemo",
        "recursive/flint-v1.0:free",
        "poolside/laguna-s-2.1:free",
        "mistralai/mistral-nemo",
        "inclusionai/ling-3.0-flash",
        "openai/gpt-oss-120b"
    ],

    "groq": [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b"
    ],
    "local": []
}

chosenModel = save.get("selectedModel") or save.get("defaultModel", "")
enabled_providers = save.get("enabledProviders", [])
enabled_models = [
    model
    for provider, models in availableModels.items()
    if provider == "local" or provider in enabled_providers
    for model in models
]
if chosenModel not in enabled_models:
    chosenModel = enabled_models[0] if enabled_models else ""
model_name = chosenModel.split("/")[-1].replace("-", " ") if chosenModel else "assistant"

_base_system_prompt = f"""You are {model_name}, a helper AI in the Epo Playground app.
    Respond to user in a nice, polite way, listen to it. You cannot commit anything illegal.
    Never use emojis or emoticons. Do not output Unicode emoji characters, ASCII emoticons, or emoji shortcodes such as :smile:.
    Use plain ASCII characters only. Do not use Unicode punctuation or typographic variants such as the non-breaking hyphen (U+2011); use standard ASCII punctuation instead.
    If user meows, meow to it back.

    Basic information:
    - Epo Playground is made by Project Aurly
    - Current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    Markdown formatting DOES NOT WORK in this app. Do not use it. Do not use any formatting, just plain text.
    User's name: {save['username']}

    User prompt:
    """

systemPrompt = _base_system_prompt