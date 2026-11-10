"""PostToolUse(Edit|Write|Bash|PowerShell): conta edições por arquivo desde o último teste rodado.
>= 5 edições no mesmo arquivo sem teste -> avisa o agente (guarda contra loop de falha, TokenEconomizer 2610.22732)."""
import json, os, re, sys, tempfile

try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
f = os.path.join(tempfile.gettempdir(), f"claude-loop-{d.get('session_id', 'x')}.json")
try:
    st = json.load(open(f))
except (OSError, ValueError):
    st = {}
ti = d.get('tool_input', {})
aviso = None
if d.get('tool_name') in ('Bash', 'PowerShell'):
    if re.search(r'pytest|npm test|go test|_test\.py|unittest|ctest', ti.get('command', '')):
        st = {}  # rodou teste: zera contagem
else:
    p = ti.get('file_path', '')
    st[p] = st.get(p, 0) + 1
    if st[p] in (5, 10):
        aviso = (f"{st[p]} edições em {os.path.basename(p)} sem rodar teste. "
                 "Pare, rode o teste ou releia o erro antes de editar de novo.")
json.dump(st, open(f, 'w'))
if aviso:
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': aviso}}))
