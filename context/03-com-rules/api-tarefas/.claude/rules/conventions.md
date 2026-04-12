# Convenções — api-tarefas

## Nomenclatura

- Arquivos e pastas: kebab-case (`task-service.js`, `not-found.js`)
- Variáveis e funções: camelCase (`findById`, `createTask`)
- Constantes: UPPER_SNAKE_CASE (`MAX_TITLE_LENGTH`)

## Validação de entrada

- Sempre validar antes de passar para o service
- Retornar 400 com mensagem descritiva quando inválido
- Nunca confiar no que veio do `req.body` sem checar

## Tratamento de erros

- Usar `next(err)` em todos os catches das rotas
- Handler global de erros em `src/middleware/error-handler.js`
- Erros conhecidos com status code explícito (404, 422, 409)
- Erros inesperados sempre 500, sem vazar stack trace para o cliente

## IDs

- UUIDs (crypto.randomUUID()) — nunca sequencial
- Razão: sequencial expõe volume e é previsível em URLs públicas

## Respostas

- 200 para leituras com resultado
- 201 para criação bem-sucedida, com o recurso criado no body
- 204 para deleção bem-sucedida, sem body
- 404 quando o recurso não existe, com `{ error: "Task not found" }`
