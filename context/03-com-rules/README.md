# 03 — Com múltiplas rules

Agora o CLAUDE.md importa duas rules: `conventions.md` e `error-handling.md`.

A diferença para o `02-com-contexto/` é sutil mas importante: antes havia uma rule.
Agora há duas, e elas se complementam. O Claude aplica as duas em conjunto,
sem precisar ser lembrado de nenhuma delas.

```bash
cd api-tarefas
claude
```

## O que está configurado

**`CLAUDE.md`** com dois `@imports`:
- `conventions.md` — nomenclatura, IDs, status codes, respostas
- `error-handling.md` — `AppError`, handler global, nunca `res.status()` no catch

## Os mesmos pedidos — observe a composição

### 1. Adicionar um endpoint de atualização

```
Adiciona um endpoint para atualizar uma tarefa existente.
```

Observe: o Claude agora aplica as duas rules ao mesmo tempo.
Usa UUID? Usa `next(err)`? Usa `AppError` com status code correto? Retorna 404 bem formado?

---

### 2. Adicionar validação de entrada

```
O endpoint de criação não valida nada. Adiciona validação para garantir
que o campo "title" é obrigatório e tem no máximo 100 caracteres.
```

Observe: ele lança `AppError(400, 'Title is required')` em vez de responder direto?
Cria middleware em `src/middleware/`? O formato de erro segue `{ "error": "..." }`?

---

### 3. Adicionar testes

```
Cria testes para as rotas existentes.
```

Observe: testa os casos de erro (400, 404) além do happy path?
Os testes usam o mesmo formato de resposta de erro que a rule define?

---

### 4. Estruturar melhor o projeto

```
O projeto está tudo em app.js. Organiza isso em uma estrutura melhor.
```

Observe: ele cria `src/middleware/error-handler.js` automaticamente?
O `AppError` aparece sem você ter pedido?

---

## O que muda quando há mais de uma rule

Com uma rule, o Claude segue aquele conjunto de convenções.
Com duas rules que se complementam, ele começa a tomar decisões que dependem
das duas ao mesmo tempo — sem você ter conectado os pontos.

Isso é o que o livro chama de **composição de contexto**.
