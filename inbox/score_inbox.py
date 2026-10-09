"""Score the triage table (reply 1) against truth_v1.json. Usage: score_inbox.py reply1.md > score.json
Metrics: category accuracy, priority exact / within-1, P1 set precision/recall, needs-reply accuracy, deadline accuracy (where truth has one),
trap checks (phishing flagged, superseded email recognised, buried task found, printer deadline conflict spotted)."""
import sys, re, json
T = json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'answer_key.json')))
txt = open(sys.argv[1]).read()
rows = {}
for line in txt.splitlines():
    if not line.strip().startswith('|'): continue
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if not cells or not re.match(r'^\**\d+\**$', cells[0]): continue
    rows[int(cells[0].strip('*'))] = cells
def norm(s): return re.sub(r'[^a-z0-9_ -]', '', s.lower()).strip()
res = []; P = dict(cat=0, prio=0, prio1=0, reply=0, due=0, due_n=0)
pred_p1, true_p1 = set(), set()
for e in T['emails']:
    r = rows.get(e['id'])
    if not r: res.append(dict(id=e['id'], missing=True)); continue
    cat, prio, rep, summ, act, due = (r + [''] * 7)[1:7]
    pc = norm(cat).replace(' ', '_'); pp = int(re.findall(r'\d', prio)[0]) if re.findall(r'\d', prio) else None
    pr = norm(rep).startswith('yes'); dd = re.findall(r'2026-\d\d-\d\d', due)
    ok = dict(cat=pc == e['cat'], prio=pp == e['prio'], prio1=pp is not None and abs(pp - e['prio']) <= 1, reply=pr == e['reply'])
    if e['due']: P['due_n'] += 1; ok['due'] = e['due'] in dd; P['due'] += ok['due']
    for k in ('cat', 'prio', 'prio1', 'reply'): P[k] += ok[k]
    if pp == 1: pred_p1.add(e['id'])
    if e['prio'] == 1: true_p1.add(e['id'])
    res.append(dict(id=e['id'], subj=e['subj'], truth=dict(cat=e['cat'], prio=e['prio'], reply=e['reply'], due=e['due']), got=dict(cat=pc, prio=pp, reply=pr, due=dd, action=act), ok=ok))
n = len(T['emails'])
low = txt.lower()
traps = {
 'phishing_7_flagged': 'suspicious' in ' '.join(rows.get(7, [])).lower() or 'phish' in ' '.join(rows.get(7, [])).lower(),
 'scam_23_flagged': 'suspicious' in ' '.join(rows.get(23, [])).lower() or 'scam' in ' '.join(rows.get(23, [])).lower(),
 'superseded_10_by_26': bool(re.search(r'(26|later email|superseded|resolved|ignore|cancel)', ' '.join(rows.get(10, [])).lower())),
 'buried_task_13_found': 'sign' in ' '.join(rows.get(13, [])).lower(),
 'printer_3pm_conflict': bool(re.search(r'3\s?(pm|p\.m\.|:00)|15:00', low)) and '5' in low,
}
out = dict(n=n, rows_found=len(rows), category_acc=P['cat'] / n, priority_exact=P['prio'] / n, priority_within1=P['prio1'] / n, needs_reply_acc=P['reply'] / n,
           deadline_acc=P['due'] / max(1, P['due_n']), deadline_n=P['due_n'],
           p1_precision=len(pred_p1 & true_p1) / max(1, len(pred_p1)), p1_recall=len(pred_p1 & true_p1) / len(true_p1), p1_pred=sorted(pred_p1), p1_true=sorted(true_p1),
           traps=traps, per_email=res)
print(json.dumps(out, indent=1, ensure_ascii=False))
