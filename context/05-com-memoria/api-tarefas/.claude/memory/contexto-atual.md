# Contexto atual do projeto

O que o Claude precisa saber sobre o estado atual antes de começar a trabalhar.

## O que já existe

- `src/app.js` — entrada da aplicação, registra rotas
- `src/routes/tasks.js` — CRUD de tarefas (GET, POST, PUT, DELETE)
- `src/services/tasks-service.js` — lógica em memória com UUIDs
- `src/middleware/error-handler.js` — handler global de erros com `AppError`
- `src/routes/tasks.test.js` — testes com Supertest, cobertura completa

## O que está pendente

- Validação de entrada no endpoint POST (title obrigatório, max 100 chars)
- Endpoint de busca por status (filtrar tarefas concluídas vs pendentes)
- Paginação no GET /tasks

## Decisões já tomadas

Ver `.claude/memory/decisoes.md`

## Última sessão

Criamos o CRUD completo de tarefas e os testes passam todos.
O próximo passo é adicionar validação de entrada antes de qualquer outra feature.
