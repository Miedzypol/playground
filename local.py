import time
from pathlib import Path
from config import MENU_STYLE
from prompt_toolkit.shortcuts import radiolist_dialog
from config import _base_system_prompt, APP_DIR, LOCAL_MODELS_DIR, LOCAL_MODELS_REGISTRY, availableModels
import requests
import sessionhandle as sh

try:
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

    def _update_system_prompt(model_system_prompt=""):
        global systemPrompt
        if model_system_prompt:
            systemPrompt = f"{_base_system_prompt}\n\nModel-Specific Instructions:\n{model_system_prompt}"
        else:
            systemPrompt = _base_system_prompt
        if sh.messages and sh.messages[0].get("role") == "system":
            sh.messages[0]["content"] = systemPrompt

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
        if local_entry not in availableModels["local"]:
            availableModels["local"].append(local_entry)
        chosenModel = local_entry
        _update_system_prompt(model_system_prompt)
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
            if model_id not in availableModels["local"]:
                availableModels["local"].append(model_id)

    
except Exception as error:
    raise Exception(f"FAIL\n{error}") from error