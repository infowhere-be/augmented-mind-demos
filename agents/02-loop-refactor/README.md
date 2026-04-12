# 02 — Loop Agentic: Refatorar Código Existente

Demo do padrão de **loop agentic aplicado a código existente**.

## O que este demo mostra

O mesmo padrão de loop do `01-loop-create`, mas em direção oposta: em vez de criar
arquivos do zero, o modelo recebe arquivos existentes e aplica transformações neles.

Isso ilustra que o loop agentic não é um padrão apenas para geração — é um padrão
para qualquer tarefa que exige múltiplas ações sequenciais sobre o sistema de arquivos.

## Como rodar

```bash
# Refatorar um arquivo específico
python3 refactor.py "Adicionar Lombok e injeção por construtor" \
  --files output/entity/Foo.java

# Refatorar múltiplos arquivos seguindo um guideline
python3 refactor.py "Aplicar o guideline" --guideline guideline.md \
  --files output/entity/Foo.java output/service/FooService.java
```

Os arquivos são sobrescritos no lugar com as alterações aplicadas.

## O que observar

- O modelo lendo o conteúdo dos arquivos antes de decidir o que mudar
- Cada alteração sendo aplicada arquivo por arquivo
- O contexto acumulando: pedido original + arquivos lidos + alterações já feitas

## Configuração

As mesmas constantes de `01-loop-create/create.py` — editar no topo de `refactor.py`.
