# Context — O impacto do CLAUDE.md

Demos do **Apêndice B — Na prática: seu agente de programação**.

Dois projetos idênticos. Mesmo código. Mesma ferramenta. Mesmos pedidos.
A única diferença é o que o Claude recebe antes de começar a trabalhar.

## Demos

### [`01-sem-contexto/`](./01-sem-contexto/)

O projeto `api-tarefas` sem nenhuma instrução. O Claude trabalha com
julgamento próprio — escolhe estrutura, convenções e frameworks por conta.

### [`02-com-contexto/`](./02-com-contexto/)

O mesmo projeto com `CLAUDE.md` e uma rule importada. O Claude segue
as convenções do projeto sem precisar ser lembrado a cada pedido.

## Como usar

Abra cada pasta em terminais separados, faça os mesmos pedidos,
e compare o que é gerado. Os READMEs de cada pasta têm os pedidos
prontos para copiar.
