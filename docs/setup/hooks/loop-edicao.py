"""PostToolUse(Edit|Write|Bash|PowerShell): counts edits per file since the last test run.
>= 5 edits to the same file without a test -> warns the agent (guard against a failure loop, TokenEconomizer 2610.22732)."""
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
        st = {}  # ran a test: reset the count
else:
    p = ti.get('file_path', '')
    st[p] = st.get(p, 0) + 1
    if st[p] in (5, 10):
        aviso = (f"{st[p]} edits to {os.path.basename(p)} without running a test. "
                 "Stop, run the test or reread the error before editing again.")
json.dump(st, open(f, 'w'))
if aviso:
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PostToolUse', 'additionalContext': aviso}}))
