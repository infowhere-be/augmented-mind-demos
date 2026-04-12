# 02 — Com contexto

O mesmo projeto `api-tarefas` — mas agora com um `CLAUDE.md` na raiz
e uma rule importada com convenções específicas.

O Claude lê tudo isso antes de qualquer interação. Use os mesmos pedidos
do `01-sem-contexto/` e compare as respostas.

```bash
cd api-tarefas
claude
```

---

## O que está configurado

**`CLAUDE.md`** — lido automaticamente ao iniciar qualquer sessão:
- Stack e versões
- Estrutura de pastas esperada
- Convenções gerais

**`.claude/rules/conventions.md`** — importado via `@` no CLAUDE.md:
- Nomenclatura de arquivos e funções
- Como tratar erros (`next(err)`, nunca `res.status()` no catch)
- IDs em UUID, nunca sequencial
- Status codes esperados por operação

---

## Os mesmos pedidos — veja a diferença

### 1. Adicionar um endpoint de atualização

```
Adiciona um endpoint para atualizar uma tarefa existente.
```

Agora observe: ele segue a estrutura `routes/` + `services/`?
Usa UUID? Retorna 200 com o recurso atualizado? Usa `next(err)` nos erros?

---

### 2. Adicionar validação de entrada

```
O endpoint de criação não valida nada. Adiciona validação para garantir
que o campo "title" é obrigatório e tem no máximo 100 caracteres.
```

Agora observe: retorna 400 com mensagem descritiva? Cria middleware separado
em `src/middleware/`? A resposta de erro segue o formato `{ error: "..." }`?

---

### 3. Adicionar testes

```
Cria testes para as rotas existentes.
```

Agora observe: usa Jest + Supertest conforme definido? O arquivo de teste
fica em `tasks.test.js` ao lado de `tasks.js`? Testa os casos de erro também?

---

### 4. Estruturar melhor o projeto

```
O projeto está tudo em app.js. Organiza isso em uma estrutura melhor.
```

Agora observe: ele segue exatamente `routes/`, `services/`, `middleware/`?
Os nomes de arquivo estão em kebab-case? O `app.js` ficou só com o registro de rotas?

---

## Por que a diferença importa

O Claude não ficou mais inteligente entre um projeto e outro.
O modelo é exatamente o mesmo. O que mudou foi o que ele recebeu antes de começar.

Com contexto, ele não precisa inventar. Ele executa com base no que você já sabe
que funciona para o seu projeto.
