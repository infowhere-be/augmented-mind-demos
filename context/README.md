# Context — O ecossistema do Claude Code

Demos do **Apêndice B — Na prática: seu agente de programação**.

Cinco versões do mesmo projeto `api-tarefas`. Mesmo código. Mesma ferramenta.
Cada etapa adiciona uma camada do ecossistema do Claude Code e mostra o que muda.

## A progressão

| Etapa | O que tem | O que o Claude faz diferente |
|-------|-----------|------------------------------|
| [`01-sem-contexto/`](./01-sem-contexto/) | Nada | Inventa estrutura, convenções e decisões |
| [`02-com-contexto/`](./02-com-contexto/) | CLAUDE.md básico (stack + estrutura) | Segue a stack, respeita a arquitetura |
| [`03-com-rules/`](./03-com-rules/) | + duas rules importadas | Aplica convenções sem ser lembrado |
| [`04-com-skills/`](./04-com-skills/) | + skill `/criar-tarefa` | Executa procedimentos que você definiu uma vez |
| [`05-com-memoria/`](./05-com-memoria/) | + arquivos de memória | Trabalha como se conhecesse o projeto há semanas |

## Como usar

Cada pasta tem um `README.md` com os pedidos para experimentar.
Abra as pastas em terminais separados e compare as respostas para o mesmo pedido.

O objetivo não é decorar os arquivos. É sentir a diferença que cada camada faz —
e entender por que um Claude com contexto não é um Claude mais inteligente,
é um Claude com mais informação.
