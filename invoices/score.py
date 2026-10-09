"""The Handoff Test · Pilot A scorer (deterministic).
Usage: python3 score.py <outputs.json | outputs_dir> [--label NAME] [--subset ids.txt]
outputs: a JSON array (or a directory of *.json arrays, concatenated) following PROMPT_v1_FROZEN.md.
Writes results/<label>/score.json, per_invoice.csv, errors.csv and prints a summary.
Rules (frozen before any model run):
 - fields scored: vendor_id, invoice_number, invoice_date, due_date, currency, net_total, tax_total, gross_total
 - normalisation: strip/case-fold strings, invoice numbers ignore spaces; amounts parsed as Decimal to the cent
 - date fields on date_ambiguity invoices: "unknown" OR the true date both count as correct
 - invoice_number on missing_invoice_number invoices: "unknown"/empty is correct
 - missing invoice / malformed object => all its fields wrong, no anomalies
 - anomaly scoring per (invoice, type); off-list types counted separately, never as true positives
 - severity: Critical = vendor_id, currency, gross_total wrong, or a missed duplicate_number/resent_verbatim/handwritten_total;
   Medium = invoice_date, due_date, invoice_number, net_total, tax_total wrong; headline = % invoices with >=1 Critical error
"""
import sys, os, re, json, csv, glob, hashlib
from decimal import Decimal, InvalidOperation
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TRUTH = os.path.join(HERE, 'dataset', 'truth.json')
TYPES = ['duplicate_number', 'resent_verbatim', 'vat_miscalc', 'totals_mismatch', 'handwritten_total', 'foreign_currency', 'date_ambiguity', 'missing_invoice_number']
FIELDS = ['vendor_id', 'invoice_number', 'invoice_date', 'due_date', 'currency', 'net_total', 'tax_total', 'gross_total']
CRIT_FIELDS = {'vendor_id', 'currency', 'gross_total'}
CRIT_MISS = {'duplicate_number', 'resent_verbatim', 'handwritten_total'}
UNKNOWN = {'', 'unknown', 'none', 'null', 'n/a'}

def amt(x):
    try:
        return Decimal(str(x).replace(',', '').strip()).quantize(Decimal('0.01'))
    except (InvalidOperation, ValueError):
        return None

def s(x): return '' if x is None else str(x).strip().casefold()

BMAP = os.path.join(HERE, 'batches', 'batch_map.csv')
def batch_lookup():
    if not os.path.exists(BMAP): return {}, {}
    m, order = {}, {}
    for k, r in enumerate(csv.DictReader(open(BMAP))):
        m[(r['batch'].upper(), int(r['page']))] = r['invoice_id']; order[r['invoice_id']] = k
    return m, order

def file_to_id(f, bm):
    f = str(f).strip()
    mp = re.match(r'^(?:HandoffTest_)?Part\s*([12])\S*?\s*[,;:_ -]*\s*p(?:age)?\s*(\d+)$', f, re.I)
    if mp and bm:
        g = (int(mp.group(1)) - 1) * 100 + int(mp.group(2))
        return bm.get((f'B{(g - 1) // 10 + 1:02d}', (g - 1) % 10 + 1))
    mm = re.match(r'^(B\d{2})(?:\.pdf)?\s*[,;:_ -]*\s*p(?:age)?\s*(\d+)$', f, re.I)
    if mm and bm: return bm.get((mm.group(1).upper(), int(mm.group(2))))
    return os.path.basename(f).replace('.pdf', '').upper()

def load_outputs(path):
    files = sorted(glob.glob(os.path.join(path, '*.json'))) if os.path.isdir(path) else [path]
    out = {}
    for f in files:
        try:
            data = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for o in data if isinstance(data, list) else []:
            if isinstance(o, dict) and o.get('file'):
                k = file_to_id(o['file'], BM)
                if k: out.setdefault(k, o)  # first answer wins
    return out

def field_ok(f, t, o):
    if o is None: return False
    v = o.get(f)
    if f == 'vendor_id': return s(v) == s(t['canonical_vendor_id'])
    if f == 'invoice_number':
        if t['invoice_number'] is None: return s(v) in UNKNOWN
        return s(v).replace(' ', '') == s(t['invoice_number']).replace(' ', '')
    if f in ('invoice_date', 'due_date'):
        if t['date_style'] == 'ambiguous' and s(v) in UNKNOWN: return True
        return s(v) == s(t[f])
    if f == 'currency': return s(v) == s(t['currency'])
    a = amt(v); return a is not None and a == Decimal(t[f])

def main():
    args = sys.argv[1:]
    path = args[0]
    label = args[args.index('--label') + 1] if '--label' in args else os.path.splitext(os.path.basename(path.rstrip('/')))[0]
    truth = json.load(open(TRUTH, encoding='utf-8'))
    if '--subset' in args:
        keep = set(open(args[args.index('--subset') + 1]).read().split()); truth = [t for t in truth if t['id'] in keep]
    global BM
    BM, ORDER = batch_lookup()
    outs = load_outputs(path)
    if ORDER:  # duplicates/resends can only be detected on whichever member of the pair is presented LATER
        byid = {t['id']: t for t in truth}
        for t in list(truth):
            src = t.get('duplicate_of') or t.get('resend_of')
            if src and src in byid and ORDER.get(src, 0) > ORDER.get(t['id'], 0):
                a = [x for x in t['anomalies'] if x['type'] in ('duplicate_number', 'resent_verbatim')]
                t2 = dict(byid[src]); t2['anomalies'] = list(t2['anomalies']) + a; t2['expected_flag'] = True
                t['anomalies'] = [x for x in t['anomalies'] if x not in a]; t['expected_flag'] = bool(t['anomalies'])
                byid[src] = t2; truth[[x['id'] for x in truth].index(src)] = t2
    res_dir = os.path.join(HERE, 'results', label); os.makedirs(res_dir, exist_ok=True)
    fcount = Counter(); tp = Counter(); fn = Counter(); fp = Counter(); offlist = Counter()
    per, errs = [], []
    crit_inv = strict_ok = missing = 0
    for t in truth:
        o = outs.get(t['id'])
        if o is None: missing += 1
        ok = {f: field_ok(f, t, o) for f in FIELDS}
        for f, v in ok.items(): fcount[f] += v
        true_types = {a['type'] for a in t['anomalies']}
        got = set()
        for a in (o or {}).get('anomalies') or []:
            ty = s(a.get('type') if isinstance(a, dict) else a)
            (got.add(ty) if ty in TYPES else offlist.update([ty]))
        for ty in TYPES:
            if ty in true_types and ty in got: tp[ty] += 1
            elif ty in true_types: fn[ty] += 1
            elif ty in got: fp[ty] += 1
        crit = [f for f in FIELDS if not ok[f] and f in CRIT_FIELDS] + [f'missed:{ty}' for ty in true_types & CRIT_MISS if ty not in got]
        crit_inv += bool(crit); strict_ok += all(ok.values())
        per.append(dict(id=t['id'], present=o is not None, fields_ok=sum(ok.values()), strict=all(ok.values()), critical=';'.join(crit),
                        true_anoms=';'.join(sorted(true_types)), got_anoms=';'.join(sorted(got)), difficulties=';'.join(t.get('difficulties', [])),
                        format=t['format'], layout=t['layout']))
        for f in FIELDS:
            if not ok[f]:
                errs.append(dict(id=t['id'], field=f, truth=t['canonical_vendor_id'] if f == 'vendor_id' else t[f], got=(o or {}).get(f, '<missing>'),
                                 severity='Critical' if f in CRIT_FIELDS else 'Medium', format=t['format']))
    n = len(truth)
    anom = {ty: dict(tp=tp[ty], fn=fn[ty], fp=fp[ty], recall=round(tp[ty] / (tp[ty] + fn[ty]), 3) if tp[ty] + fn[ty] else None,
                     precision=round(tp[ty] / (tp[ty] + fp[ty]), 3) if tp[ty] + fp[ty] else None) for ty in TYPES}
    T, F, P = sum(tp.values()), sum(fn.values()), sum(fp.values())
    by_fmt = defaultdict(lambda: [0, 0])
    for r in per: by_fmt[r['format']][0] += 1; by_fmt[r['format']][1] += bool(r['critical'])
    summary = dict(label=label, n=n, missing_outputs=missing,
                   truth_sha256=hashlib.sha256(open(TRUTH, 'rb').read()).hexdigest(),
                   field_accuracy={f: round(fcount[f] / n, 4) for f in FIELDS},
                   field_accuracy_overall=round(sum(fcount.values()) / (n * len(FIELDS)), 4),
                   strict_all_fields_correct=round(strict_ok / n, 4),
                   critical_error_rate=round(crit_inv / n, 4),
                   critical_error_rate_by_format={k: round(v[1] / v[0], 4) for k, v in sorted(by_fmt.items())},
                   anomaly_micro=dict(tp=T, fn=F, fp=P, recall=round(T / (T + F), 4) if T + F else None, precision=round(T / (T + P), 4) if T + P else None),
                   anomaly_by_type=anom, offlist_flags=dict(offlist))
    json.dump(summary, open(os.path.join(res_dir, 'score.json'), 'w'), indent=1)
    for name, rows in (('per_invoice.csv', per), ('errors.csv', errs)):
        with open(os.path.join(res_dir, name), 'w', newline='') as fh:
            if rows:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(json.dumps({k: summary[k] for k in ('label', 'n', 'missing_outputs', 'field_accuracy_overall', 'strict_all_fields_correct', 'critical_error_rate', 'anomaly_micro')}, indent=1))

if __name__ == '__main__':
    main()
