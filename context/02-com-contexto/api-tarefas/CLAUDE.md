# api-tarefas

API de gestão de tarefas pessoais em Node.js com Express.

## Stack

- Node.js 20+
- Express 4.x
- Jest para testes
- Sem banco de dados por enquanto — dados em memória

## Estrutura do projeto

```
src/
  app.js          # entrada da aplicação, só registra rotas
  routes/         # um arquivo por recurso (tasks.js, users.js)
  services/       # lógica de negócio, separada dos controllers
  middleware/     # validação, erros, autenticação
```

## Convenções

- Rotas finas: recebem a requisição, delegam para o service, devolvem a resposta
- Services testáveis: sem dependência do Express, só lógica pura
- Erros sempre com `next(err)` — nunca `res.status()` direto no catch
- Respostas em camelCase, datas em ISO 8601

## Testes

- Jest + Supertest para testes de rota
- Um arquivo de teste por arquivo de rota: `tasks.test.js` para `routes/tasks.js`
- Rodar com `npm test`

@.claude/rules/conventions.md
