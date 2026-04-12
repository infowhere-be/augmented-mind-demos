# Backlog — augmented-mind-demos

Código companion do livro. A ideia central: **mostrar coisas funcionando**.

Não é documentação. Não é tutorial. É o leitor abrindo o terminal,
rodando algo, e vendo com os próprios olhos o que o capítulo descreve.

Alguns demos entram no livro como referência direta. A maioria fica
aqui no repositório — o livro aponta para eles e quem quiser ir fundo, vai.

---

## O que já existe

| Pasta | Capítulo | O que mostra |
|-------|----------|--------------|
| `agents/01-loop-create/` | Cap 10 | Loop agentic gerando código Java arquivo por arquivo |
| `agents/02-loop-refactor/` | Cap 10 | Mesmo loop aplicado a refatoração |
| `context/01-sem-contexto/` | Apêndice B | Projeto sem CLAUDE.md — Claude inventa tudo |
| `context/02-com-contexto/` | Apêndice B | Mesmo projeto com CLAUDE.md + rules — Claude segue convenções |

---

## O que construir a seguir

### Prioridade alta — já está no livro, precisa de código real

#### `context/03-com-skills/` — Apêndice B
Skills como vocabulário. Pegar o mesmo `api-tarefas` e adicionar uma skill
que define um procedimento repetível. Mostrar que o Claude executa o procedimento
sem precisar ser instruído de novo.

**O que o leitor vai ver:** mesmo pedido de antes, mas agora o Claude não só segue
convenções — ele executa um fluxo inteiro que você definiu uma vez e nunca mais
precisou repetir.

---

#### `context/04-evolucao-claude-md/` — Apêndice B
O CLAUDE.md não nasce pronto. Mostrar a evolução em commits:
- v1: só o nome do projeto e a stack
- v2: adiciona estrutura de pastas e convenções
- v3: adiciona `@import` de rules
- v4: adiciona skills

Cada versão versionada, com a resposta do Claude salva em `respostas/`.
O leitor vê a diferença acumulando conforme o contexto cresce.

**Este é provavelmente o demo mais poderoso do apêndice.**

---

#### `examples/tokens/` — Cap 1 / Cap 8 (contexto finito)
Script simples que conta tokens de um texto usando a API da Anthropic.
Mostrar os três contadores: `input_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`.

**O que o leitor vai ver:** o que o livro chama de "três contadores" em número real.
Colocar um arquivo grande, ver o contexto crescer. Colocar o mesmo arquivo duas vezes,
ver o cache entrar.

---

#### `examples/rag/` — Cap 11
RAG mínimo em Python. Sem banco vetorial externo — só embeddings em memória.
- Carrega um conjunto de documentos (ex: perguntas frequentes inventadas)
- Recebe uma pergunta
- Encontra o trecho mais relevante por similaridade coseno
- Passa para o Claude junto com a pergunta
- Compara resposta com RAG vs resposta sem RAG (hallucination demo)

**O que o leitor vai ver:** o modelo respondendo errado sobre algo que não conhece,
e acertando depois que recebe o documento certo. Exatamente o exemplo do médico
sem o exame de sangue que está no cap 11.

---

### Prioridade média — iluminam conceitos importantes, não são obrigatórios

#### `examples/temperatura/` — Cap 3
Mesmo prompt, três temperaturas diferentes (0.0 / 0.7 / 1.2).
Mostrar que com temperatura 0 a resposta é determinística e que com 1.2
começa a alucinar ou divagar.

**O que o leitor vai ver:** "estocástico" deixando de ser palavra e virando
comportamento observável.

---

#### `examples/prompt-antes-depois/` — Cap 9
Dois arquivos de prompt para a mesma tarefa:
- `prompt-vago.txt` — "me ajuda com um texto"
- `prompt-preciso.txt` — com papel, audiência, tom, tamanho, objetivo

Script que envia os dois e salva as respostas em `respostas/`.
O leitor vê o que o cap 9 chama de "paisagem das respostas" em resultado concreto.

---

#### `monitor/` — Apêndice B
O `claude-monitor` mencionado no apêndice. Lê os arquivos JSONL do Claude Code
em tempo real e mostra o que está acontecendo em cada sessão.

Já existe como projeto separado (`claude-monitor` em `github-infowhere/`).
Aqui pode entrar uma versão simplificada — só a função de leitura do JSONL
com 20 linhas, para mostrar o mecanismo nu.

---

### Prioridade baixa — vale a pena mas não é urgente

#### `examples/tokenizacao/` — Cap 2
Visualizar como um texto vira tokens. Mostrar palavras comuns vs raras,
como emojis e números se comportam.

#### `examples/contexto-crescendo/` — Apêndice B
Script que manda mensagens em loop e imprime os três contadores a cada turno.
Mostrar o contexto enchendo em tempo real — o "mesa com papéis" do livro virando número.

---

## Filosofia

- Cada demo deve funcionar isolado — sem dependências entre pastas
- O README de cada pasta é a entrada do leitor — direto e sem enrolação
- Respostas do Claude salvas em `respostas/*.txt` e versionadas — o histórico é a demo
- Quando algo muda no CLAUDE.md, commitar antes de rodar o exemplo — o git conta a história
- Preferir Python simples a frameworks pesados — qualquer pessoa consegue ler
