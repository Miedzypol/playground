import sessionhandle as sh
from config import client
from click import prompt
from groq import Groq


def requestOpenRouter(prompt, model="mistralai/mistral-nemo"):
    sh.addmessage("user", prompt)
    stream = client.chat.completions.create(
        model=model,
        messages=sh.messages,
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
    sh.addmessage("assistant", full)
    return 0
def requestGroq(prompt, model="llama-3.3-70b-versatile"):
    sh.addmessage("user", prompt)
    options = {}
    if model.startswith("openai/gpt-oss-"):
        options["reasoning_effort"] = "medium"
    stream = Groq().chat.completions.create(
        model=model,
        messages=sh.messages,
        stream=True,
        **options,
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
    sh.addmessage("assistant", full)
    return 0
def requestLocalModel(prompt, model):
    raise NotImplementedError("Local model request function is not implemented yet.")



def requestAPI(prompt, chosenModel, availableModels, provider=None):
    if provider == "local" or (
        provider is None and chosenModel in availableModels["local"]
    ):
        requestLocalModel(prompt, chosenModel)
    elif provider == "openrouter":
        requestOpenRouter(prompt, chosenModel)
    elif provider == "groq":
        requestGroq(prompt, chosenModel)
    elif provider is not None:
        raise ValueError(f"Unknown model provider: {provider}")
    elif chosenModel in availableModels["openrouter"]:
        requestOpenRouter(prompt, chosenModel)
    elif chosenModel in availableModels["groq"]:
        requestGroq(prompt, chosenModel)
    return 0