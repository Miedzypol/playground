# (Epo) Playground
<img width="75" height="45" alt="playground" src="https://github.com/user-attachments/assets/6c54f686-e303-493c-8757-c2c85e470c5d" />

> **CLI for communicating with AI Agents**

Epo Playground is a command-line interface tool for interacting with AI models, inspired by Pi and OpenCode CLI interfaces. Currently uses OpenRouter API, with plans to migrate to a custom server in the future.

---

## Features

- **Interactive CLI** - Clean, colored interface with command support
- **Multiple AI Models** - Support for various models from OpenRouter
- **Local Models** - Run local GGUF models via llama-cpp-python
- **Streaming Responses** - Real-time response display
- **Session Management** - Start new sessions and clear chat history
- **System Prompts** - Configurable system prompts for different models
- **Model Downloading** - Built-in system for downloading local models
- **Auto-completion** - Intelligent command suggestions

---

## Installation

### Requirements
- Python 3.10 or higher
- pip (Python package manager)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Miedzypol/playground.git
cd playground

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment config file
cp .env.example .env

# Edit .env and add your OpenRouter API key
nano .env  # Linux/Mac
# or
notepad .env  # Windows
```

---

## Configuration

### OpenRouter API Key

1. Register at [OpenRouter](https://openrouter.ai/)
2. Generate an API key in your user panel
3. Add the key to your `.env` file:

```env
OPENROUTER_API_KEY=your_api_key_here
```

### Optional Settings

In the `.env` file, you can also define the default model:

```env
MODEL=mistralai/mistral-nemo
```

---

## Usage

### Running

```bash
python app.py
```

### Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Clear screen |
| `/exit` | Exit application |
| `/new` | Start new session (clear chat history) |
| `/model` | Change AI model |
| `/menu` | Open application menu |

### Basic Interaction

After launching, you can immediately ask questions:

```
>> Hello, how are you?

AI: Hello! I'm doing well, thank you for asking. How can I help you?

>> /model
# Opens interactive model selection

>> /new
Started new session.

>> /exit
Bye!
```

---

## Local Models

### Supported Models

The application supports local GGUF models running via `llama-cpp-python`.

### Available Model Series

- **Mosaic v1** - QuickFix-2B model

### Downloading Models

1. Select "Test local Epo models..." from the menu
2. Choose a model series (e.g., Mosaic v1)
3. The application will automatically download the model and system prompt (if available)

Models are stored in the `models/` directory with this structure:
```
models/
└── mosaic/
    └── v1/
        ├── mosaic-v1-quickfix.gguf
        └── system-prompt.md
```

### Manual Model Addition

1. Place your `.gguf` file in `models/<series>/<version>/`
2. Optionally: add a `system-prompt.md` file in the same directory
3. Launch the application - models will be automatically detected

---

## Project Structure

```
playground/
├── app.py              # Main CLI application
├── utils.py            # Utility functions
├── config.ini          # Application configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Ignored files
├── LICENSE             # License (BSD 3-Clause)
└── AGENTS.md           # AI agents guidelines
```

---

## Configuration

### config.ini

```ini
[General]
version = 1.2
default_model = mistralai/mistral-nemo
```

### Default Available Models

- `recursive/flint-v1.0:free`
- `poolside/laguna-s-2.1:free`
- `mistralai/mistral-nemo` (default)
- `inclusionai/ling-3.0-flash`
- `openai/gpt-oss-120b`

---

## Migration to Custom Server

In the future, migration from OpenRouter API to a custom server for AI model communication is planned. The application structure is prepared for this change.

---

## Contributing

Contributions are welcome! If you want to help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/name`)
3. Make changes and commit (`git commit -m 'Added new feature'`)
4. Submit a Pull Request

---

## License

The project is licensed under **BSD 3-Clause License**.

See [LICENSE](LICENSE) for details.

---

## Author

**Project Aurly** (ayllo)

---

## Contact

For questions or issues, open an Issue in the GitHub repository.

---

*Epo Playground v1.2 | (c) 2026 Project Aurly*
<img width="2400" height="2400" alt="wallpaper" src="https://github.com/user-attachments/assets/b3ed1df2-4015-4e28-be79-f07186fb8518" />
