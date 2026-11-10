"""PreToolUse(Bash): test command -> runs once, saves the log and returns only failures + summary (official cost docs).
Accepts the agent's real format: `cd X && `, `timeout N`, `py -3.x`/`python -X utf8` and suffix `2>&1 | tail -N`.
Passed: only the tail. Failed: traceback (-A 15) + tail. Log per PID (no collision when run in parallel)."""
import json, re, sys

try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
cmd = d.get('tool_input', {}).get('command', '').strip()
SEG = r'[^;&|<>`$\n]'  # no chaining, pipe, redirection, subshell or variable
m = re.fullmatch(
    r'(?P<cd>cd +(?:"[^"$`]*"|\'[^\']*\'|[^\s;&|<>`$\'"]+) *&& *)?'
    r'(?P<core>(?:timeout +\d+[smh]? +)?'
    r'(?:(?:python3?|py(?: +-3(?:\.\d+)?)?)(?: +-X +[^\s;&|<>`$]+)* +-m +pytest|pytest|npm test|go test)'
    rf'(?: {SEG}*)?)'
    r'(?: *2>&1)?(?: *\| *tail +(?:-n *)?-?(?P<n>\d+))?', cmd)
# collection/help/version: the whole output is the answer, do not filter
if m and not re.search(r'(?:^| )(?:--co|--collect-only|--help|-h|--fixtures|--markers|--version|--setup-plan)(?= |$)', m['core']):
    n = m['n'] or 3
    # failed: error lines (+15 after) and pytest `E `/`> ` lines (max 80 ~ 4 tracebacks), joined with the last n, no repeats
    awk = ("awk -v n=%s 'NR==FNR{t=NR;next} FNR>t-n{print;next} "
           "/(FAIL|ERROR|Error|error:|Traceback)/{a=FNR+15} (FNR<=a || /^[E>] /) && c++<80' \"$L\" \"$L\"") % n
    novo = (f"L=/tmp/_teste_$$.log; {m['cd'] or ''}({m['core'].strip()}) > \"$L\" 2>&1; rc=$?; "
            f"if [ $rc -eq 0 ]; then tail -n {n} \"$L\"; else {awk}; fi; echo \"exit=$rc (full log: $L)\"")
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                                             'updatedInput': {**d['tool_input'], 'command': novo}}}))
else:
    # not a test: delegate to RTK (a single hook, no competing updatedInput)
    import subprocess
    try:
        r = subprocess.run(['rtk', 'hook', 'claude'], input=json.dumps(d), capture_output=True, text=True, timeout=4)  # smaller than the hook's timeout of 5
        print(r.stdout.strip() or '{}')
    except Exception:
        print('{}')
