# Augmented Mind — Demos

Código companion do livro **"Desvendando a Mente Aumentada"** (Casa do Código).

Cada pasta é um demo auto-contido que ilustra um conceito do livro. Podem ser
executados de forma independente — não há dependências partilhadas entre pastas.

## Demos

### [`agents/`](./agents/) — Capítulo 10 (Agentes)

Loop agentic com tool calling e streaming SSE: um LLM local que gera e refactora
código Java ficheiro a ficheiro, decidindo um passo de cada vez até concluir a tarefa.

- [`01-loop-create/`](./agents/01-loop-create/) — gera código Java do zero
- [`02-loop-refactor/`](./agents/02-loop-refactor/) — aplica refactoring a código existente

### [`context/`](./context/) — Apêndice B (O ecossistema do Claude Code)

Cinco versões do mesmo projeto `api-tarefas` (Node.js/Express). Mesmo código, mesma
ferramenta — cada etapa adiciona uma camada do ecossistema do Claude Code e mostra
o que muda na resposta do agente.

- [`01-sem-contexto/`](./context/01-sem-contexto/) — sem CLAUDE.md
- [`02-com-contexto/`](./context/02-com-contexto/) — CLAUDE.md básico
- [`03-com-rules/`](./context/03-com-rules/) — + rules importadas
- [`04-com-skills/`](./context/04-com-skills/) — + skill `/criar-tarefa`
- [`05-com-memoria/`](./context/05-com-memoria/) — + ficheiros de memória

### `monitor/` e `examples/`

Reservados para demos planeados (ver [`BACKLOG.md`](./BACKLOG.md)). Ainda sem conteúdo.

## Tecnologias

- **agents/**: Python 3.11+ (gera código Java como output)
- **context/**: Node.js / Express (projecto `api-tarefas` usado como cenário)

## Requisitos

- Python 3.11+ (para os demos de `agents/`)
- Node.js (para correr o `api-tarefas` dos demos de `context/`)
- Acesso SSH a um servidor com Ollama + LiteLLM, ou adaptar a função `call_model()`
  para qualquer endpoint compatível com OpenAI

## Como usar

Cada demo tem o seu próprio `README.md` com as instruções de execução. Exemplos:

```bash
# Loop agentic (agents/)
cd agents/01-loop-create
python3 create.py "Crie um CRUD completo para RepairShop com id UUID, name e status"

# Projecto api-tarefas (context/)
cd context/01-sem-contexto/api-tarefas
npm install
npm start
```

## Livro

Publicado pela [Casa do Código](https://www.casadocodigo.com.br).
