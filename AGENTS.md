# AGENTS.md

This file provides guidelines and context for AI agents (like Mistral Vibe) interacting with this repository.

## Repository Overview
- **Name**: Epo Playground
- **Description**: CLI application for communicating with AI models via OpenRouter API (future: custom server).
- **Primary Language**: Python
- **Main File**: `app.py`

## Project Structure
```
playground/
├── app.py              # Main CLI application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── LICENSE             # BSD 3-Clause License
└── AGENTS.md           # This file
```

## Coding Guidelines
- Follow existing code style (no inline comments, minimal formatting).
- Use Python 3.10+ features where applicable.
- Prefer simple, direct solutions over complex abstractions.
- Maintain backward compatibility with existing functionality.

## Key Dependencies
- `openai` - OpenRouter API client
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management
- `prompt_toolkit` - Interactive command-line prompts

## Environment Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and add your `OPENROUTER_API_KEY`
3. Run: `python app.py`

## Common Tasks
- **Adding new commands**: Extend the `komendy` dictionary in `app.py`
- **Changing models**: Modify `chosenModel` variable or add model selection
- **Error handling**: Wrap API calls in try/except blocks

## Important Notes
- Do not add emojis in responses (per system prompt).
- Maintain Polish language support where applicable.
- Preserve existing functionality when making changes.
- Always test changes before committing.

## Version
Current version: 1.0 (defined in `app.py`)

## License
BSD 3-Clause License (see LICENSE file)
