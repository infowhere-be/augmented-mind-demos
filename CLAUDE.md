# augmented-mind-demos

Companion code para o livro **"Desvendando a Mente Aumentada"** (Casa do Código).
Cada pasta é um demo auto-contido que ilustra um conceito do livro — corre independentemente, sem dependências partilhadas entre pastas.

> **Repositório público.** Não importa regras do `standarts` (privado) — este CLAUDE.md
> é auto-contido para funcionar em qualquer clone. Mantém-no assim.

## Estrutura

| Pasta | Conteúdo |
|-------|----------|
| `agents/` | Agentic loop: LLM local que gera e refactora código Java ficheiro a ficheiro, com tool calling e streaming SSE (Capítulo 10 — Agents) |
| `monitor/` | Demo de monitorização |
| `context/` | Demos sobre janela de contexto |
| `examples/` | Exemplos avulsos |

## Convenções

- Código e comentários em inglês; documentação do livro em português (PT-BR)
- Cada demo é independente — sem `requirements.txt` partilhado
- Demos devem correr com o mínimo de setup (instruções no README de cada pasta)
- Português do Brasil na documentação (livro Casa do Código)

## Git

- Branch principal: `main`
- Commits: Conventional Commits, mensagens em português
- Sem `Co-Authored-By` de IA (convenção do livro)
