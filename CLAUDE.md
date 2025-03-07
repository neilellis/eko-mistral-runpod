# CLAUDE.md - Project Guidelines & Commands

## Commands
- **Build Docker**: `docker build --build-arg HF_TOKEN=your_huggingface_token -t eko-mistral-runpod:local .`
- **Run Docker**: `docker run -p 8000:8000 eko-mistral-runpod:local`
- **Test Endpoint**: `python test.py --url http://localhost:8000/run --prompt "Your prompt"`
- **Lint**: `flake8 src/ test.py`
- **Type Check**: `mypy src/ test.py`

## Style Guidelines
- **Imports**: Group standard library, third-party, then local imports
- **Formatting**: Use 4 spaces for indentation
- **Types**: Add type annotations for function parameters and returns
- **Naming**: snake_case for variables/functions, CamelCase for classes
- **Error Handling**: Use try/except with specific exceptions
- **Documentation**: Docstrings for all functions and classes
- **Constants**: Use uppercase with underscores
- **Line Length**: Maximum 100 characters