

from pyexpat.errors import messages

from click import prompt


def requestOpenRouter(prompt, model="mistralai/mistral-nemo"):
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
    return 0
def requestGroq(prompt, model="llama-3.3-70b-versatile"):
    raise NotImplementedError("Groq API request function is not implemented yet.")
def requestLocalModel(prompt, model):
    raise NotImplementedError("Local model request function is not implemented yet.")


"""OLD REQUEST API FUNC:
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
            messages.append({"role": "assistant", "content": full})"""

def requestAPI(prompt, chosenModel, availableModels):
    if chosenModel in availableModels["local"]:
        requestLocalModel(prompt, chosenModel)
    elif chosenModel in availableModels["openrouter"]:
        requestOpenRouter(prompt, chosenModel)
    elif chosenModel in availableModels["groq"]:
        requestGroq(prompt, chosenModel)
    return 0