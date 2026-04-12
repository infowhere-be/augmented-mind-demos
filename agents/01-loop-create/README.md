# 01 — Loop Agentic: Gerar Código do Zero

Demo do padrão de **loop agentic com tool calling**.

## O que este demo mostra

O modelo recebe um pedido em linguagem natural e entra em loop:

```
pedido
  └── LLM decide: chamar escrever_arquivo("entity/Foo.java", "...")
        └── arquivo criado no disco
              └── LLM decide: chamar escrever_arquivo("service/FooService.java", "...")
                    └── arquivo criado no disco
                          └── LLM decide: chamar finalizar("Gerados 8 arquivos")
                                └── loop encerra
```

O modelo nunca escreve todo o código de uma vez. Ele toma uma decisão por passo,
observa o resultado, e decide o próximo. Isso é o loop agentic.

## Como rodar

```bash
# Sem guideline — modelo usa julgamento próprio
python3 create.py "Crie um CRUD completo para RepairShop com id UUID, name e status"

# Com guideline — modelo segue as regras do arquivo
python3 create.py "Crie um CRUD completo para RepairShop" --guideline guideline.md
```

O código gerado aparece em `output/` ao final.

## O que observar

- Cada passo do loop impresso no terminal com número de mensagens no contexto
- O modelo chamando `escrever_arquivo` para cada classe separadamente
- A diferença entre rodar com e sem `--guideline` (arquitetura em camadas, Lombok, etc.)
- O contexto crescendo a cada iteração — o modelo relê tudo a cada passo

## Configuração

Editar as constantes no topo de `create.py`:

| Constante | Descrição |
|-----------|-----------|
| `MODEL` | Nome do modelo no LiteLLM/Ollama |
| `API_KEY` | Chave para o gateway |
| `CLOUDFLARED` | Caminho do binário cloudflared |
| `OUTPUT_DIR` | Onde os arquivos gerados são salvos |
