# Agents — Java Code Generator & Refactorer

Two agentic scripts that use a local LLM to generate or refactor Java/Spring Boot code.
The model runs in a tool-calling loop, writing one file at a time until it calls `finalizar`.

## How it works

```
User request
    ↓
LLM (tool calling loop)
    ├── escrever_arquivo("entity/Foo.java", "...") → writes file
    ├── escrever_arquivo("service/FooService.java", "...") → writes file
    └── finalizar("Generated 8 files") → done
```

Responses stream token by token via SSE (`stream: true` + `curl -sN`).

## Scripts

### `create.py` — Generate new code

```bash
# Without guideline
python3 create.py "Create a full CRUD for RepairShop with id UUID, name and status enum"

# With guideline
python3 create.py "Create a full CRUD for RepairShop" --guideline guideline.md
```

### `refactor.py` — Refactor existing code

```bash
# Without guideline
python3 refactor.py "Add Lombok and constructor injection" --files output/entity/Foo.java

# With guideline
python3 refactor.py "Apply the guideline" --guideline guideline.md \
  --files output/entity/Foo.java output/service/FooService.java
```

## Configuration

Edit the constants at the top of each script:

| Constant | Description |
|----------|-------------|
| `MODEL` | Model name as exposed by LiteLLM/Ollama |
| `API_KEY` | API key for the Kong gateway |
| `CLOUDFLARED` | Path to cloudflared binary (for SSH tunnel) |
| `OUTPUT_DIR` | Where generated files are written (default: `./output/`) |

## Output

Generated files are written to `./output/` and printed to the terminal at the end.
The folder is wiped on each run.
