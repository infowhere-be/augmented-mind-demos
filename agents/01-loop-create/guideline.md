# Java/Spring Boot Coding Standards — InfoWhere

> Padroes de codigo Java compartilhados entre todos os projetos InfoWhere.
> Versao: 1.2.0 | Data: 19/02/2026

---

## Versao e Stack

- Java 21
- Spring Boot 3.3+
- Maven para build
- PostgreSQL 16 como banco de dados

## Naming Conventions

| Elemento | Convencao | Exemplo |
|----------|-----------|---------|
| Classes | PascalCase | `InvoiceService`, `CustomerController` |
| Interfaces | PascalCase | `FalcoGateway`, `InvoiceRepository` |
| Metodos | camelCase | `findById`, `syncCustomers` |
| Constantes | UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS`, `DEFAULT_PAGE_SIZE` |
| Packages | lowercase | `be.infowhere.finance.service` |
| Enums | PascalCase (valores UPPER_SNAKE_CASE) | `PaymentStatus.NOT_PAID` |
| Arquivos | PascalCase (match class name) | `InvoiceService.java` |

## Idioma

- Codigo e commits: **ingles**
- Documentacao: **portugues**

## Arquitetura em Camadas

```
Controller → Facade → Service → Repository/Gateway
     ↓           ↓                    ↓
    DTO      Mapper              Entity/External Model
```

### Responsabilidades

| Camada | Responsabilidade |
|--------|-----------------|
| Controller | Receber HTTP, validacao de entrada (Bean Validation), retornar DTOs |
| Facade | Orquestracao de services, conversao DTO/Entity via Mapper, transacoes |
| Service | Logica de negocio, chamadas a APIs externas, regras de sync |
| Repository | Spring Data JPA, queries customizadas, paginacao |
| Gateway | Comunicacao com APIs externas, retry, rate limiting |
| Mapper | MapStruct para conversao DTO/Entity |

## Estrutura de Packages

```
be.infowhere.{project}/
├── config/              # SecurityConfig, CacheConfig, WebConfig
├── controller/          # REST controllers
├── facade/              # Orquestracao
├── service/             # Logica de negocio
├── repository/          # Spring Data JPA
├── entity/              # JPA entities
│   └── enums/           # Enums do dominio
├── dto/                 # Data Transfer Objects
├── mapper/              # MapStruct mappers
├── gateway/             # Comunicacao externa
│   └── generated/       # OpenAPI Generator (excluido de testes)
└── exception/           # Custom exceptions
```

## DTOs e Entities

### Entity (JPA)

```java
@Entity
@Table(name = "invoices")
@Getter @Setter
@NoArgsConstructor
public class Invoice {
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true)
    private UUID falcoId;

    @Enumerated(EnumType.STRING)
    private InvoiceStatus status;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}
```

### DTO

```java
public record InvoiceDTO(
    UUID id,
    String number,
    DocumentType documentType,
    InvoiceStatus status,
    BigDecimal totalAmount,
    LocalDate documentDate
) {}
```

### Mapper (MapStruct)

```java
@Mapper(componentModel = "spring")
public interface InvoiceMapper {
    InvoiceDTO toDto(Invoice entity);
    List<InvoiceDTO> toDtoList(List<Invoice> entities);
}
```

## Collections e Stream API

### Preferir `Collectors.toMap()` com `Function.identity()` em vez de `Set`

Quando se precisa de lookup por chave a partir de uma lista, preferir `Map` com `Function.identity()` em vez de `Set`. O Map da lookup O(1) **e** acesso ao objecto completo — o Set so responde "existe ou nao".

```java
// PREFERIDO — Map com Function.identity()
// Lookup O(1) + acesso ao objecto completo
Map<String, Contract> contractsByRef = contracts.stream()
    .collect(Collectors.toMap(Contract::getReference, Function.identity()));

// Uso: obter o objecto directamente
Contract previous = contractsByRef.get("SC 28330");
if (previous != null) {
    newContract.setPreviousContract(previous);
}

// EVITAR — Set so responde sim/nao
Set<String> existingRefs = contracts.stream()
    .map(Contract::getReference)
    .collect(Collectors.toSet());

// Limitado: sabe que existe, mas precisa de outra query para obter o objecto
if (existingRefs.contains("SC 28330")) {
    // Precisa de findByReference() extra...
}
```

### Quando usar cada abordagem

| Abordagem | Quando usar |
|-----------|-------------|
| `Collectors.toMap(key, Function.identity())` | Lookup por chave + acesso ao objecto (preferido) |
| `Collectors.toMap(key, value)` | Transformar lista em Map com valor derivado |
| `Collectors.toSet()` | Apenas verificar existencia (sem precisar do objecto) |
| `Collectors.groupingBy(key)` | Agrupar multiplos objectos pela mesma chave |

### Outras preferencias com Streams

```java
// Preferir method references a lambdas quando possivel
list.stream().map(Contract::getReference)       // BOM
list.stream().map(c -> c.getReference())        // EVITAR

// Preferir toList() (Java 16+) a Collectors.toList()
list.stream().filter(predicate).toList()        // BOM (imutavel)
list.stream().filter(predicate).collect(Collectors.toList())  // EVITAR (verboso)
```

---

## CQS / SOLID

### Command Query Separation (CQS)

Metodos de servico devem ser claramente **queries** ou **commands** — nunca misturar os dois sem comunicar o efeito lateral no nome.

| Tipo | Anotacao | Regra |
|------|----------|-------|
| Query | `@Transactional(readOnly = true)` | Nunca modifica estado. `find*`, `get*`, `list*`, `search*` sao queries puras. |
| Command | `@Transactional` | Modifica estado (save, delete, update). |
| Hybrid (find-or-create) | `@Transactional` | DEVE usar nomes que comuniquem o efeito: `findOrCreate*`, `findOrCreate*`, `getOrCreate*`. |

```java
// CORRECTO — query pura, nome comunica ausencia de efeitos
@Transactional(readOnly = true)
public Collection<Tag> findAllByCodes(Collection<String> codes) {
    return repository.findAllByCodeIn(codes);
}

// CORRECTO — hibrido com nome explicito que comunica o efeito lateral
@Transactional
public Collection<Tag> findOrCreateAllByCodes(Collection<String> codes) {
    // faz find-or-create: nome "resolve" comunica que pode criar
    ...
}

// ERRADO — nome e "find" mas tem saveAll() escondido dentro
@Transactional
public Collection<Tag> findAllByCodes(Collection<String> codes) {
    // VIOLACAO CQS: saveAll() escondido num metodo com nome de query
    repository.saveAll(newTags);
    ...
}
```

---

## Persistence Layer — Query Approaches

### Order of preference

| Approach | When to use |
|----------|-------------|
| **Derived query methods** | Simple lookups by 1-2 fixed fields (findByEmail, findByStatus) |
| **JPA Specifications** | Dynamic filtering with optional/combinable parameters |
| **JdbcTemplate** | Aggregations, CTEs, reports, or performance-critical bulk reads |

### JPA Specifications (preferred for dynamic filtering)

When an endpoint accepts **optional or combinable filters**, always use `Specification<T>` from Spring Data JPA (`org.springframework.data.jpa.domain.Specification`).

**Setup:**

1. Repository must extend `JpaSpecificationExecutor<T>`
2. Create a `*Specifications` class with static factory methods
3. Each method returns `Specification<T>`, returning `null` inside the lambda to make the filter neutral

```java
// Repository
public interface InvoiceRepository extends JpaRepository<Invoice, UUID>,
        JpaSpecificationExecutor<Invoice> {
}

// Specifications class
public class InvoiceSpecifications {

    @Nonnull
    public static Specification<Invoice> hasStatus(@Nullable final InvoiceStatus status) {
        return (root, query, cb) -> {
            if (status == null) {
                return null; // neutral: ignored when not provided
            }
            return cb.equal(root.get("status"), status);
        };
    }

    @Nonnull
    public static Specification<Invoice> hasCustomerName(@Nullable final String name) {
        return (root, query, cb) -> {
            if (name == null || name.isBlank()) {
                return null;
            }
            return cb.like(cb.lower(root.get("customerName")), "%" + name.toLowerCase() + "%");
        };
    }
}

// Controller — composing filters
final Specification<Invoice> spec = Specification.allOf(
        hasStatus(status),
        hasCustomerName(customerName));
final Page<Invoice> result = repository.findAll(spec, pageable);
```

**Key rules:**
- Use `Specification.allOf()` for AND composition, `Specification.anyOf()` for OR
- Use `Specification.unrestricted()` for a no-op specification (NOT `Specification.where(null)`, which is deprecated)
- Each specification method must handle `null`/empty parameters gracefully by returning `null`

---

## Database Migrations (Flyway)

- Flyway com SQL puro (nao usar Hibernate ddl-auto em producao)
- Convencao: `V{version}__{description}.sql`
- Hibernate: `ddl-auto: validate` em runtime

```
src/main/resources/db/migration/
├── V1__create_customer_table.sql
├── V2__create_invoice_table.sql
└── V3__create_sync_log_table.sql
```

### Regra Critica: Flyway e apenas para DDL (schema), nunca DML (dados)

**NUNCA usar Flyway para corrigir dados incorrectos em producao.** Flyway e uma ferramenta de controlo de versao de schema — serve para criar tabelas, adicionar colunas, criar indices, renomear campos. Nao serve para corrigir dados lancados erroneamente.

| Tipo | O que e | Vai para Flyway? |
|------|---------|-----------------|
| **DDL** | `CREATE TABLE`, `ALTER COLUMN`, `ADD INDEX`, `DROP CONSTRAINT` | **Sim** |
| **DML de bootstrap** | `INSERT` de dados de referencia obrigatorios (ex: categorias iniciais, roles) | **Sim, com criterio** |
| **DML de correcao** | `UPDATE`/`DELETE` para corrigir dados lancados erroneamente | **NAO — nunca** |

**Correcoes de dados devem ser executadas directamente na base de dados como SQL avulso.** Razoes:

1. Dados errados sao incidentes pontuais — nao fazem parte do schema evolutivo
2. Uma migration Flyway corre em TODOS os ambientes (dev, staging, prod) — um UPDATE pode ter efeitos inesperados em ambientes com dados diferentes
3. Migrations DML sao mais dificeis de testar — um `LIKE '%RADIUS%'` case-sensitive pode funcionar num ambiente e falhar silenciosamente noutro
4. Uma migration incorrecta (bug no SQL) fica permanente no `flyway_schema_history` e pode ser confusa para futuros developers

**Procedimento para correcao de dados em producao:**

```bash
# 1. Ligar directamente ao PostgreSQL via Docker
ssh ssh.infowhere.be "docker exec -it infowhere-postgres psql -U admin -d finance"

# 2. Verificar o que vai ser alterado (SELECT antes do UPDATE)
SELECT id, beneficiary, category_id FROM bank_statement_import_transaction
WHERE beneficiary ILIKE '%radius%';

# 3. Executar o UPDATE
UPDATE bank_statement_import_transaction
SET category_id = (SELECT id FROM expense_category WHERE code = 'ELECTRICIDADE_EV')
WHERE beneficiary ILIKE '%radius%'
  AND category_id = (SELECT id FROM expense_category WHERE code = 'INTERNET_PROXIMUS');

# 4. Verificar resultado
SELECT COUNT(*) FROM bank_statement_import_transaction
WHERE beneficiary ILIKE '%radius%'
  AND category_id = (SELECT id FROM expense_category WHERE code = 'INTERNET_PROXIMUS');
-- Deve retornar 0
```

**Origem desta regra**: Incidente Radius (2026-03-25) — a transaccao "Radius Business Solutions (Belgium) NV" foi corrigida 3 vezes via Flyway (V76, V77, V78) com erros consecutivos, resultando em deploys repetidos para o mesmo problema. V76 tinha um bug de case-sensitivity (`LIKE` vs `ILIKE`) e nao actualizava `categoryId`. A correcao final foi feita directamente na BD com SQL avulso em minutos.

### Regra Critica: Nunca modificar ficheiros de migration ja aplicados

**NUNCA editar um ficheiro `.sql` de migration depois de ter sido aplicado em qualquer ambiente — nem para corrigir um typo, nem para adicionar comentarios.**

O Flyway calcula um checksum (CRC32) do conteudo de cada ficheiro. Qualquer alteracao — incluindo adicionar ou remover um comentario `--` — muda o checksum. Na proxima vez que a aplicacao arrancar, o Flyway detecta mismatch entre o checksum em `flyway_schema_history` e o checksum do ficheiro local e **recusa-se a iniciar**. A aplicacao entra em crash loop.

```
-- ISTO DERRUBA A APLICACAO EM PRODUCAO:
-- (adicionar qualquer comentario a um ficheiro ja aplicado)
-- Flyway checksum mismatch for migration version N
-- -> Applied to database : -1067892965
-- -> Resolved locally    : 131904711
```

**Se precisar de documentar que uma migration estava errada**: escrever no session log, `DECISIONS.md` ou `CONTEXT.md` — nunca no proprio ficheiro `.sql`.

**Se o ficheiro ja foi modificado por engano e a aplicacao nao arranca**, a correcao e actualizar os checksums directamente na BD:

```bash
# Verificar os checksums "locais" (novos) no erro do Flyway:
# "Resolved locally: XXXXXX" — esse e o valor correcto agora

ssh ssh.infowhere.be "docker exec -i infowhere-postgres psql -U admin -d finance -c \"
UPDATE flyway_schema_history SET checksum = <checksum_local> WHERE version = 'N';
SELECT version, checksum FROM flyway_schema_history WHERE version = 'N';
\""
```

**Origem desta regra**: Incidente 2026-03-25 — apos o incidente Radius, foram adicionados comentarios de aviso aos ficheiros V76/V77/V78 ja aplicados. Isso mudou os checksums e derrubou o `finance-backend` em producao. Fix: `UPDATE flyway_schema_history` com os checksums novos.

## Seguranca

### Spring Security + Keycloak

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health", "/actuator/info", "/actuator/prometheus").permitAll()
                .anyRequest().authenticated()
            )
            .build();
    }
}
```

## Error Handling

### Global Exception Handler

```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiResponse> handleNotFound(ResourceNotFoundException e) {
        return ResponseEntity.status(404)
            .body(new ApiResponse(false, null, e.getMessage()));
    }
}
```

## Cache

- Caffeine como implementacao de cache
- TTL padrao: 15 minutos
- Cache invalidado apos sync

## Metricas (Prometheus / Micrometer)

Todo servico Spring Boot deve expor metricas Prometheus. Ver `observability.md` para arquitetura completa.

### Dependencia (pom.xml)

`spring-boot-starter-actuator` ja deve estar presente. Adicionar o registry Prometheus:

```xml
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

### Configuracao (application.yml)

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  metrics:
    tags:
      application: ${spring.application.name}
```

### Custom Metrics

```java
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;

@Service
public class SyncService {
    private final Counter syncCounter;
    private final Timer syncTimer;

    public SyncService(MeterRegistry registry) {
        this.syncCounter = Counter.builder("finance_sync_total")
            .description("Total sync operations")
            .tag("type", "invoice")
            .register(registry);
        this.syncTimer = Timer.builder("finance_sync_duration_seconds")
            .description("Sync duration")
            .register(registry);
    }

    public void syncInvoices() {
        syncTimer.record(() -> {
            // logica de sync
            syncCounter.increment();
        });
    }
}
```

### Security Config

Permitir acesso anonimo ao endpoint de metricas (ja incluido no exemplo de SecurityConfig acima):

```java
.requestMatchers("/actuator/health", "/actuator/info", "/actuator/prometheus").permitAll()
```

## Gateway Pattern (APIs externas)

```java
public interface FalcoGateway {
    List<FalcoInvoice> listInvoices(int page, int pageSize);
    FalcoInvoice getInvoice(UUID id);
}

@Service
@Retryable(maxAttempts = 3, backoff = @Backoff(delay = 1000, multiplier = 2))
public class FalcoGatewayImpl implements FalcoGateway {
    // Rate limiter: 50 req/min
    // Logging de chamadas
}
```

## Testes

- JUnit 5 + Mockito
- Cobertura minima: **85% (JaCoCo)**
- Exclusoes: `gateway/generated/**`, `config/**`, `*Application.class`

| Camada | Tipo | Framework |
|--------|------|-----------|
| Controller | `@WebMvcTest` | MockMvc + Security |
| Facade | Unit | Mockito |
| Service | Unit | Mockito |
| Repository | `@DataJpaTest` | H2 |
| Mapper | Unit | - |
| Gateway | Unit | Mockito |

### Profile de Teste

```yaml
# application-test.yml
spring:
  datasource:
    url: jdbc:h2:mem:testdb;MODE=PostgreSQL
  flyway:
    enabled: false
```

## Comandos

```bash
# Build
mvn clean package

# Testes
mvn test

# Testes com cobertura
mvn verify  # JaCoCo report em target/site/jacoco/

# Rodar aplicacao
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

---

*InfoWhere Standards v1.2.0*
