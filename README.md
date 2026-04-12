# Augmented Mind — Demos

Companion code for the book **"Desvendando a Mente Aumentada"** (Casa do Código).

Each folder contains a self-contained demo that illustrates a concept from the book.
You can run them independently — no shared dependencies between folders.

## Demos

### [`agents/`](./agents/)

Agentic loop demos: a local LLM that generates and refactors Java code file by file,
using tool calling and streaming SSE. Covers the concepts in **Chapter 10 — Agents**.

### [`monitor/`](./monitor/)

Claude Monitor — a terminal UI that shows Claude's thinking process in real time.

### [`examples/`](./examples/)

Additional standalone examples added throughout the book.

## Requirements

- Python 3.11+
- SSH access to a server running Ollama + LiteLLM (or adapt the `call_model()` function
  to point to any OpenAI-compatible endpoint)

## Book

Published by [Casa do Código](https://www.casadocodigo.com.br).
