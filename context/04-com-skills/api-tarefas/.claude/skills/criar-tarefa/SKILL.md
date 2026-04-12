# Skill — criar-tarefa

Cria um novo endpoint de recurso no projeto `api-tarefas`, seguindo
o padrão de rotas + service + testes estabelecido no projeto.

## Uso

```
/criar-tarefa <nome-do-recurso>
```

Exemplo: `/criar-tarefa comentario` cria o endpoint `/comentarios` completo.

## O que esta skill faz

1. Cria `src/routes/<recurso>.js` com os endpoints GET, POST, PUT, DELETE
2. Cria `src/services/<recurso>-service.js` com a lógica em memória
3. Registra a rota em `src/app.js`
4. Cria `src/routes/<recurso>.test.js` com testes para cada endpoint
5. Confirma que `npm test` passa antes de declarar concluído

## Regras que esta skill segue

- Rotas delegam tudo para o service — sem lógica nas rotas
- Service usa `crypto.randomUUID()` para IDs
- Erros são lançados como `AppError` e tratados pelo handler global
- Testes cobrem: criação, listagem, busca por ID, atualização, deleção e 404
