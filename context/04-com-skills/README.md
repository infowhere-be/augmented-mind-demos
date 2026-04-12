# 04 — Com skills

Além do CLAUDE.md e das rules, agora há uma skill: `/criar-tarefa`.

Uma skill é um procedimento que você definiu uma vez e pode invocar sempre que precisar.
Em vez de descrever o que fazer toda vez, você invoca o nome — e o Claude executa
o procedimento completo, do jeito que você especificou.

```bash
cd api-tarefas
claude
```

## O que está configurado

Tudo do `03-com-rules/`, mais:

**`.claude/skills/criar-tarefa/SKILL.md`** — procedimento para criar um novo recurso:
1. Cria a rota
2. Cria o service
3. Registra em `app.js`
4. Cria os testes
5. Confirma que tudo passa

## Experimente invocar a skill

```
/criar-tarefa comentario
```

Observe: o Claude cria tudo de uma vez — rota, service, testes — seguindo
o padrão do projeto, sem que você tenha descrito nada disso.

Compare com fazer o mesmo pedido em texto livre:

```
Cria um CRUD completo para comentários com rota, service e testes.
```

A diferença: com a skill, o Claude sabe exatamente o que "completo" significa
para o seu projeto. Com texto livre, ele decide por conta.

---

## Os pedidos anteriores, com a skill disponível

### Adicionar validação de entrada

```
O endpoint de criação não valida nada. Adiciona validação para garantir
que o campo "title" é obrigatório e tem no máximo 100 caracteres.
```

A skill não cobre validação — mas as rules sim. O Claude combina as duas coisas.

---

### Criar um endpoint novo completo

```
/criar-tarefa projeto
```

Observe o que o Claude faz passo a passo. É exatamente o que está na skill,
na ordem que você definiu.

---

## O que uma skill muda

Sem skill: você descreve o procedimento toda vez. Com chance de esquecer um passo.
Com skill: você invoca um nome. O procedimento está definido, testado, e é consistente.

Skills são **experiência codificada**. O capítulo sobre memória explica por quê isso importa.
