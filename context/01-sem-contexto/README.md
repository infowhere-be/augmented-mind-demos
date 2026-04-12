# 01 — Sem contexto

Projeto `api-tarefas` sem nenhuma instrução para o Claude.

Abra este diretório com o Claude Code e experimente os pedidos abaixo.
O Claude vai responder com boas intenções — mas vai inventar as convenções,
escolher estrutura por conta própria, e tomar decisões que podem não se
alinhar com o que você queria.

```bash
cd api-tarefas
claude
```

---

## Pedidos para experimentar

### 1. Adicionar um endpoint de atualização

```
Adiciona um endpoint para atualizar uma tarefa existente.
```

Observe: que status code ele usa? Como valida a entrada? Usa UUID ou ID sequencial?
Onde coloca a lógica — no arquivo de rotas ou separa em outro lugar?

---

### 2. Adicionar validação de entrada

```
O endpoint de criação não valida nada. Adiciona validação para garantir
que o campo "title" é obrigatório e tem no máximo 100 caracteres.
```

Observe: como ele retorna o erro? Qual status code? A mensagem é genérica ou descritiva?
Ele cria um middleware separado ou coloca a validação inline na rota?

---

### 3. Adicionar testes

```
Cria testes para as rotas existentes.
```

Observe: que framework ele escolhe? Como organiza os arquivos de teste?
Vai testar só o happy path ou também os casos de erro?

---

### 4. Estruturar melhor o projeto

```
O projeto está tudo em app.js. Organiza isso em uma estrutura melhor.
```

Observe: que estrutura ele inventa? Como nomeia as pastas?
Separa rotas de lógica de negócio, ou não?

---

Compare as respostas com o que o mesmo projeto produz em `02-com-contexto/`.
