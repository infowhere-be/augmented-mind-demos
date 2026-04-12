# Rule — Tratamento de Erros

Esta rule é carregada automaticamente. O Claude aplica sem precisar ser lembrado.

## Handler global

Todo projeto tem um `src/middleware/error-handler.js`. Erros chegam lá via `next(err)`.
Nunca capturar erro numa rota e responder diretamente com `res.status()`.

## Formato de resposta de erro

```json
{ "error": "Mensagem descritiva para o cliente" }
```

Nunca expor stack trace, nome de classe ou detalhe interno na resposta.

## Status codes

| Situação | Status |
|----------|--------|
| Recurso não encontrado | 404 |
| Dados inválidos | 400 |
| Conflito (já existe) | 409 |
| Erro inesperado | 500 |

## Erros conhecidos vs inesperados

Criar uma classe `AppError` com `statusCode` e `message`.
Lançar `new AppError(404, 'Task not found')` nas rotas.
O handler global distingue `AppError` (responde com o status) de outros (responde 500).
