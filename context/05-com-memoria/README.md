# 05 — Com memória

A última camada: arquivos de memória importados no CLAUDE.md.

O projeto agora tem contexto acumulado — decisões que foram tomadas, o que já existe,
o que está pendente. O Claude lê tudo isso antes de qualquer interação e trabalha
como se conhecesse o projeto há semanas.

```bash
cd api-tarefas
claude
```

## O que está configurado

Tudo do `04-com-skills/`, mais:

**`.claude/memory/decisoes.md`** — decisões já tomadas (IDs em UUID, sem banco, sem auth).
O Claude não vai sugerir ID sequencial. Não vai perguntar sobre banco de dados.
Não vai propor autenticação que você ainda não quer.

**`.claude/memory/contexto-atual.md`** — estado do projeto agora.
O que já existe, o que está pendente, o que foi feito na última sessão.

Ambos importados via `@` no CLAUDE.md.

---

## Experimente começar uma nova sessão

Abra o Claude neste projeto e pergunte:

```
O que falta fazer neste projeto?
```

Observe: o Claude responde com base no `contexto-atual.md`, não no que ele acha
que um projeto típico precisaria. Ele sabe que a validação está pendente.
Ele sabe que a paginação ainda não existe.

---

```
Por que estamos usando UUID em vez de ID sequencial?
```

Observe: o Claude responde com a justificativa que está em `decisoes.md`,
não com uma explicação genérica sobre UUIDs.

---

```
Adiciona a validação de entrada que está pendente.
```

Observe: o Claude sabe exatamente o que "a validação que está pendente" é,
porque leu o contexto. Não precisa perguntar.

---

## O ponto central

O Claude não ficou mais inteligente. O modelo é o mesmo de sempre.

O que mudou é que ele chegou a esta sessão com o histórico do projeto —
não porque ele "lembrou", mas porque alguém registrou e colocou à disposição.

É exatamente o que o Capítulo 10 descreve:
**a IA não constrói experiência. Ela executa com base na experiência que você coloca à disposição.**

---

## Compare a jornada completa

| Etapa | O que o Claude tem | O que muda |
|-------|--------------------|------------|
| `01-sem-contexto` | Nada | Inventa tudo |
| `02-com-contexto` | CLAUDE.md básico | Segue a stack |
| `03-com-rules` | + rules específicas | Aplica convenções sem ser lembrado |
| `04-com-skills` | + skills | Executa procedimentos definidos por você |
| `05-com-memoria` | + memória | Trabalha como se conhecesse o projeto |
