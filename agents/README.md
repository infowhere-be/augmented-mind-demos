# Agents — Loop Agentic com Tool Calling

Demos do **Capítulo 10 — Agentes**.

Um agente não responde. Ele age: chama uma ferramenta, observa o resultado, decide o
próximo passo, repete. Este diretório mostra esse padrão em funcionamento — um modelo
de linguagem que escreve arquivos Java, um por vez, até considerar a tarefa concluída.

## Demos

### [`01-loop-create/`](./01-loop-create/)

O agente recebe um pedido e gera código Java do zero, arquivo por arquivo,
usando tool calling e streaming SSE.

### [`02-loop-refactor/`](./02-loop-refactor/)

O agente recebe arquivos Java existentes e aplica refatorações, seguindo
as mesmas ferramentas e o mesmo padrão de loop.

## Requisitos

- Python 3.11+
- Acesso SSH a um servidor com Ollama + LiteLLM
  (ou adaptar `call_model()` para qualquer endpoint OpenAI-compatible)
