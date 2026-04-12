# Decisões do projeto

Registro de decisões tomadas ao longo do desenvolvimento.
O Claude lê isso e não precisa perguntar o que já foi decidido.

## IDs

**Decisão:** usar `crypto.randomUUID()`, nunca ID sequencial.
**Por quê:** IDs sequenciais expõem o volume de dados e são previsíveis em URLs públicas.
**Data:** primeira semana do projeto.

## Banco de dados

**Decisão:** dados em memória por enquanto. Sem PostgreSQL nem SQLite.
**Por quê:** o foco é na estrutura de rotas e serviços, não na persistência.
**Quando mudar:** quando houver necessidade de persistir entre restarts.

## Autenticação

**Decisão:** sem autenticação por enquanto.
**Por quê:** o projeto ainda está em fase de estruturação.
**Quando mudar:** antes de qualquer deploy público.

## Testes

**Decisão:** Jest + Supertest. Um arquivo de teste por arquivo de rota.
**Por quê:** Supertest permite testar rotas sem subir o servidor de verdade.
**Cobertura mínima:** todos os endpoints + casos de erro (404, 400).
