"""
Agente refatorador de codigo Java existente.

Uso:
  python3 refactor.py "Adiciona Lombok e injecao por construtor" --files output/entity/Foo.java
  python3 refactor.py "Segue o guideline" --guideline guideline.md --files output/entity/Foo.java output/service/FooService.java
"""

import argparse
import json
import subprocess
import os
import sys
import shutil
import tempfile
import time
import threading
import uuid

# ── Configuracao ──────────────────────────────────────────────────────────────

MODEL       = "hf.co/bartowski/DeepSeek-Coder-V2-Lite-Instruct-GGUF:Q4_K_M"
API_KEY     = "HfjW1QbcM3rPtdLpX7smXccEKc7dQGFe"
CLOUDFLARED = "/usr/local/Cellar/cloudflared/2026.1.2/bin"
OUTPUT_DIR  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")

# ── Cores ─────────────────────────────────────────────────────────────────────

CYAN   = "\033[0;36m"
GREEN  = "\033[0;32m"
YELLOW = "\033[0;33m"
RED    = "\033[0;31m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

# ── Spinner ───────────────────────────────────────────────────────────────────

class Spinner:
    def __init__(self, label="Aguardando modelo"):
        self._running = False
        self._thread  = None
        self._label   = label

    def start(self):
        self._running = True
        self._thread  = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        print()

    def _spin(self):
        start = time.time()
        while self._running:
            elapsed = int(time.time() - start)
            mins, secs = elapsed // 60, elapsed % 60
            timer = f"{mins}m{secs:02d}s" if mins > 0 else f"{secs}s"
            print(f"\r  {DIM}{self._label}... {timer}{RESET}", end="", flush=True)
            time.sleep(1)

# ── Ferramentas ───────────────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "escrever_arquivo",
            "description": (
                "Salva a versao refatorada de um arquivo Java no diretorio de output. "
                "Use um arquivo por classe. Chame para cada classe refatorada."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Caminho relativo, ex: entity/RepairShop.java"
                    },
                    "content": {
                        "type": "string",
                        "description": "Conteudo completo do arquivo Java refatorado"
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "finalizar",
            "description": "Indica que todos os arquivos foram refatorados. Chame apenas quando tiver reescrito tudo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Resumo das refatoracoes aplicadas"
                    }
                },
                "required": ["message"]
            }
        }
    }
]

# ── Executar ferramenta ───────────────────────────────────────────────────────

def execute_tool(name: str, args: dict, created_files: list) -> str:
    if name == "escrever_arquivo":
        path    = args.get("path", "unknown.java")
        content = args.get("content", "")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        full_path = os.path.join(OUTPUT_DIR, path)
        parent    = os.path.dirname(full_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        created_files.append(path)
        return f"Arquivo '{path}' salvo ({len(content)} bytes)."
    if name == "finalizar":
        return "FINALIZADO"
    return f"Ferramenta '{name}' nao reconhecida."

# ── Chamada ao modelo (streaming SSE) ────────────────────────────────────────

def call_model(messages: list) -> dict:
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "stream": True,
        "temperature": 0.1,
    }

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    tmp.write(json.dumps(payload))
    tmp.close()

    env = os.environ.copy()
    env["PATH"] = CLOUDFLARED + ":" + env.get("PATH", "")

    cmd_str = (
        f"cat {tmp.name} | ssh ssh.infowhere.be "
        f"'curl -sN http://localhost:8000/ai/v1/chat/completions "
        f"-H \"Content-Type: application/json\" "
        f"-H \"apikey: {API_KEY}\" "
        f"-d @-'"
    )

    accumulated_content = ""
    tool_calls_raw: dict = {}

    try:
        process = subprocess.Popen(
            cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, env=env,
        )

        for line in process.stdout:
            line = line.rstrip("\n")
            if not line.startswith("data: "):
                continue
            data_str = line[6:]
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            delta = chunk.get("choices", [{}])[0].get("delta", {})

            if delta.get("content"):
                accumulated_content += delta["content"]
                print("\r\033[K", end="", flush=True)
                print(delta["content"], end="", flush=True)

            for tc_delta in (delta.get("tool_calls") or []):
                idx = tc_delta.get("index", 0)
                if idx not in tool_calls_raw:
                    tool_calls_raw[idx] = {"id": "", "name": "", "arguments": ""}
                if tc_delta.get("id"):
                    tool_calls_raw[idx]["id"] = tc_delta["id"]
                fn = tc_delta.get("function", {})
                tool_calls_raw[idx]["name"]      += fn.get("name", "")
                tool_calls_raw[idx]["arguments"] += fn.get("arguments", "")

        process.wait()
        if accumulated_content:
            print()

    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass

    if process.returncode != 0:
        stderr = process.stderr.read() if process.stderr else ""
        print(f"\n  {RED}Erro SSH/curl: {stderr[:300]}{RESET}")
        return {}

    tool_calls = []
    for tc in sorted(tool_calls_raw.values(), key=lambda x: x["id"]):
        if not tc["name"]:
            continue
        try:
            args = json.loads(tc["arguments"]) if tc["arguments"] else {}
        except json.JSONDecodeError:
            args = {}
        tool_calls.append({
            "id": tc["id"] or f"call_{uuid.uuid4().hex[:16]}",
            "type": "function",
            "function": {"name": tc["name"], "arguments": args},
        })

    return {"role": "assistant", "content": accumulated_content, "tool_calls": tool_calls}

# ── Resumo final ──────────────────────────────────────────────────────────────

def print_summary(steps: int, files: list, final_message: str = ""):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  RESULTADO{RESET}")
    print(f"  Passos:   {steps}")
    print(f"  Arquivos: {len(files)}")

    if files:
        print(f"  Output:   {CYAN}{OUTPUT_DIR}/{RESET}\n")
        for f in files:
            print(f"    {GREEN}+{RESET} {f}")

    if final_message:
        print(f"\n  {YELLOW}Notas do agente:{RESET}")
        print(f"  {DIM}{final_message}{RESET}")

    if files:
        print(f"\n{YELLOW}  Conteudo gerado:{RESET}")
        for f in files:
            full = os.path.join(OUTPUT_DIR, f)
            print(f"\n{CYAN}  ── {f} ──{RESET}")
            try:
                with open(full, "r") as fh:
                    for line in fh:
                        print(f"  {DIM}{line}{RESET}", end="")
            except OSError:
                print(f"  {RED}(nao foi possivel ler o arquivo){RESET}")

    print(f"\n{BOLD}{'='*60}{RESET}\n")

# ── Agente principal ──────────────────────────────────────────────────────────

def run(user_request: str, guideline_path: str | None, file_paths: list[str]):
    guideline = ""
    if guideline_path:
        if not os.path.isfile(guideline_path):
            print(f"{RED}Guideline nao encontrado: {guideline_path}{RESET}")
            sys.exit(1)
        with open(guideline_path, "r") as f:
            guideline = f.read()

    # Ler conteudo dos arquivos a refatorar
    files_content = []
    for fp in file_paths:
        if not os.path.isfile(fp):
            print(f"{RED}Arquivo nao encontrado: {fp}{RESET}")
            sys.exit(1)
        with open(fp, "r") as f:
            content = f.read()
        files_content.append((fp, content))

    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    if guideline:
        system_prompt = (
            "Voce e um desenvolvedor Java senior especialista em Spring Boot 3.x.\n"
            "Refatore o codigo fornecido seguindo rigorosamente o guideline abaixo.\n\n"
            "Regras obrigatorias:\n"
            "- Use Lombok: @RequiredArgsConstructor, @Value, @Builder, @Slf4j, @Data\n"
            "- Injecao por construtor SEMPRE. Nunca @Autowired em campo.\n"
            "- DTOs como Java Records ou classes imutaveis com @Value + @Builder\n"
            "- Sempre crie interface antes da implementacao para Services\n"
            "- Constantes e campos no TOPO da classe, antes dos metodos\n"
            "- Modificador mais restritivo possivel\n"
            "- Enums para dados de catalogo\n"
            "- Constantes nomeadas para numeros e strings magicas\n"
            "- Collection<T> como padrao; List<T> apenas com JPA Specification\n"
            "- Todo codigo, comentarios e identificadores em INGLES\n\n"
            "Salve cada arquivo refatorado usando escrever_arquivo.\n"
            "Ao terminar tudo, chame finalizar com um resumo das mudancas.\n\n"
            f"--- GUIDELINE COMPLETO ---\n{guideline}"
        )
    else:
        system_prompt = (
            "Voce e um desenvolvedor Java senior especialista em Spring Boot 3.x.\n"
            "Refatore o codigo fornecido aplicando boas praticas de producao.\n\n"
            "Salve cada arquivo refatorado usando escrever_arquivo.\n"
            "Ao terminar tudo, chame finalizar com um resumo das mudancas."
        )

    # Montar mensagem do usuario com os arquivos
    files_block = "\n\n".join(
        f"// FILE: {fp}\n{content}"
        for fp, content in files_content
    )
    full_request = f"{user_request}\n\n{files_block}" if files_content else user_request

    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  REFACTOR — REFATORADOR DE CODIGO JAVA{RESET}")
    print(f"  Modelo:    {CYAN}{MODEL}{RESET}")
    print(f"  Guideline: {CYAN}{guideline_path or '(nenhum)'}{RESET}")
    print(f"  Arquivos:  {CYAN}{len(files_content)} arquivo(s){RESET}")
    print(f"  Output:    {CYAN}{OUTPUT_DIR}/{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    print(f"\n{YELLOW}[INSTRUCAO]{RESET}")
    print(f"  {user_request}\n")
    if files_content:
        print(f"{YELLOW}[ARQUIVOS DE ENTRADA]{RESET}")
        for fp, content in files_content:
            print(f"  {GREEN}~{RESET} {fp} ({len(content)} bytes)")
        print()
    print(f"{YELLOW}[LOOP AGENTIC]{RESET}")
    print(f"  {DIM}Streaming SSE. O modelo refatora arquivo por arquivo.{RESET}\n")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": full_request},
    ]

    step          = 0
    created_files = []
    final_message = ""

    while True:
        step += 1
        print(f"{CYAN}── Passo {step} ──────────────────────────────────────{RESET}")
        print(f"  Mensagens no contexto: {len(messages)}")

        spinner = Spinner("Refatorando codigo")
        spinner.start()
        msg = call_model(messages)
        spinner.stop()

        if not msg:
            print(f"  {RED}Sem resposta. Parando.{RESET}")
            break

        tool_calls = msg.get("tool_calls", [])
        content    = msg.get("content", "")

        if tool_calls:
            msg_for_history = {
                "role": "assistant",
                "content": msg.get("content") or None,
                "tool_calls": [
                    {
                        "id": tc.get("id", f"call_{tc.get('function',{}).get('name','')}"),
                        "type": "function",
                        "function": {
                            "name": tc.get("function", {}).get("name", ""),
                            "arguments": (
                                tc.get("function", {}).get("arguments")
                                if isinstance(tc.get("function", {}).get("arguments"), str)
                                else json.dumps(tc.get("function", {}).get("arguments", {}))
                            ),
                        },
                    }
                    for tc in tool_calls
                ],
            }
            messages.append(msg_for_history)

            for tc in tool_calls:
                fn        = tc.get("function", {})
                tool_name = fn.get("name", "")
                tool_args = fn.get("arguments", {})
                tool_id   = tc.get("id", f"call_{tool_name}")

                if isinstance(tool_args, str):
                    try:
                        tool_args = json.loads(tool_args)
                    except json.JSONDecodeError:
                        tool_args = {}

                print(f"  {GREEN}Modelo chamou: {tool_name}{RESET}")

                if tool_name == "finalizar":
                    final_message = tool_args.get("message", "")
                    print(f"  {GREEN}Concluido.{RESET}")
                    print_summary(step, created_files, final_message)
                    return

                if tool_name == "escrever_arquivo":
                    path = tool_args.get("path", "?")
                    size = len(tool_args.get("content", ""))
                    print(f"  {GREEN}  + {path} ({size} bytes){RESET}")

                result = execute_tool(tool_name, tool_args, created_files)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "content": result,
                })

        elif content:
            print(f"\n  {YELLOW}Modelo respondeu em texto (sem tool call):{RESET}")
            print(f"  {DIM}{content[:400]}{RESET}\n")
            break
        else:
            print(f"  {RED}Resposta vazia. Parando.{RESET}")
            break

        if step >= 20:
            print(f"\n  {YELLOW}Limite de 20 passos atingido.{RESET}")
            break

    print_summary(step, created_files, final_message)

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refatora codigo Java existente com ou sem guideline.")
    parser.add_argument("request", nargs="+", help="Descricao das refatoracoes a aplicar")
    parser.add_argument("--guideline", metavar="PATH", default=None,
                        help="Caminho para o arquivo de guideline (opcional)")
    parser.add_argument("--files", metavar="FILE", nargs="+", default=[],
                        help="Arquivos Java a refatorar")
    args = parser.parse_args()

    run(" ".join(args.request), args.guideline, args.files)
