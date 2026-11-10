"""PreToolUse(Bash): comando de teste -> roda uma vez, guarda o log e devolve só falhas + resumo (doc oficial de custos).
Aceita o formato real do agente: `cd X && `, `timeout N`, `py -3.x`/`python -X utf8` e sufixo `2>&1 | tail -N`.
Passou: só o tail. Falhou: traceback (-A 15) + tail. Log por PID (não colide em paralelo)."""
import json, re, sys

try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
cmd = d.get('tool_input', {}).get('command', '').strip()
SEG = r'[^;&|<>`$\n]'  # sem encadeamento, pipe, redireção, subshell ou variável
m = re.fullmatch(
    r'(?P<cd>cd +(?:"[^"$`]*"|\'[^\']*\'|[^\s;&|<>`$\'"]+) *&& *)?'
    r'(?P<core>(?:timeout +\d+[smh]? +)?'
    r'(?:(?:python3?|py(?: +-3(?:\.\d+)?)?)(?: +-X +[^\s;&|<>`$]+)* +-m +pytest|pytest|npm test|go test)'
    rf'(?: {SEG}*)?)'
    r'(?: *2>&1)?(?: *\| *tail +(?:-n *)?-?(?P<n>\d+))?', cmd)
# coleta/ajuda/versão: a saída inteira é a resposta, não filtrar
if m and not re.search(r'(?:^| )(?:--co|--collect-only|--help|-h|--fixtures|--markers|--version|--setup-plan)(?= |$)', m['core']):
    n = m['n'] or 3
    # falhou: linhas do erro (+15 depois) e linhas `E `/`> ` do pytest (máx 80 ~ 4 tracebacks), unidas às últimas n, sem repetir
    awk = ("awk -v n=%s 'NR==FNR{t=NR;next} FNR>t-n{print;next} "
           "/(FAIL|ERROR|Error|error:|Traceback)/{a=FNR+15} (FNR<=a || /^[E>] /) && c++<80' \"$L\" \"$L\"") % n
    novo = (f"L=/tmp/_teste_$$.log; {m['cd'] or ''}({m['core'].strip()}) > \"$L\" 2>&1; rc=$?; "
            f"if [ $rc -eq 0 ]; then tail -n {n} \"$L\"; else {awk}; fi; echo \"exit=$rc (log completo: $L)\"")
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                                             'updatedInput': {**d['tool_input'], 'command': novo}}}))
else:
    # não é teste: delega ao RTK (um hook só, sem updatedInput concorrente)
    import subprocess
    try:
        r = subprocess.run(['rtk', 'hook', 'claude'], input=json.dumps(d), capture_output=True, text=True, timeout=4)  # menor que o timeout 5 do hook
        print(r.stdout.strip() or '{}')
    except Exception:
        print('{}')
