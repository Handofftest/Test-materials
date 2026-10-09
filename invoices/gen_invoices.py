"""The Handoff Test · Pilot A · synthetic invoice generator (seeded, reproducible).
All companies, people, tax IDs and IBANs are FICTIONAL (tax IDs use an invalid 'TEST-' prefix).
Outputs: invoices/INV-###.pdf (+ .png preview), truth.json, truth.csv, manifest.csv, SHA256 of truth files.
Usage: python3 gen_invoices.py [seed] [n]"""
import sys, os, json, csv, random, hashlib, math, datetime as dt
from decimal import Decimal, ROUND_HALF_UP
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 20261008
N = int(sys.argv[2]) if len(sys.argv) > 2 else 200
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset')
G = os.environ.get('FONTS_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')) + '/'  # Google Fonts (OFL) folders: inter/, jetbrainsmono/, manrope/, dmsans/, ibmplexmono/
R = random.Random(SEED)

def F(name, size, w=None):
    paths = {'inter': 'inter/Inter[opsz,wght].ttf', 'mono': 'jetbrainsmono/JetBrainsMono[wght].ttf', 'manrope': 'manrope/Manrope[wght].ttf',
             'dmsans': 'dmsans/DMSans[opsz,wght].ttf', 'plex': 'ibmplexmono/IBMPlexMono-Regular.ttf'}
    p = G + paths[name]
    if not os.path.exists(p):
        import glob; p = (glob.glob(G + name + '/*.ttf') or glob.glob(G + 'inter/*.ttf'))[0]
    f = ImageFont.truetype(p, size)
    if w:
        try:
            axes = f.get_variation_axes(); vals = []
            for a in axes:
                n = a.get('name', b'')
                n = n.decode() if isinstance(n, bytes) else str(n)
                vals.append(w if 'eight' in n.lower() or n.lower().startswith('w') else a.get('default', 14))
            f.set_variation_by_axes(vals)
        except Exception: pass
    return f

D2 = Decimal('0.01')
def q(x): return Decimal(x).quantize(D2, rounding=ROUND_HALF_UP)

# ---------------- fictional world ----------------
VENDORS = [
    ('V01', ['Brightwell Office Supply Ltd', 'BRIGHTWELL OFFICE SUPPLY LTD', 'Brightwell Office Supply Limited'], 'GBP'),
    ('V02', ['Nordhaven Logistik GmbH', 'NORDHAVEN LOGISTIK GMBH', 'Nordhaven Logistik'], 'EUR'),
    ('V03', ['Casa Albarel S.L.', 'CASA ALBAREL SL', 'Casa Albarel Sociedad Limitada'], 'EUR'),
    ('V04', ['Pinecrest Cleaning Co.', 'PINECREST CLEANING CO', 'Pinecrest Cleaning Company'], 'USD'),
    ('V05', ['Atelier Mirelle SARL', 'ATELIER MIRELLE SARL', 'Atelier Mirelle'], 'EUR'),
    ('V06', ['Kestrel Print & Signage', 'KESTREL PRINT AND SIGNAGE', 'Kestrel Print+Signage'], 'GBP'),
    ('V07', ['Zurlinden Software AG', 'ZURLINDEN SOFTWARE AG', 'Zurlinden Software'], 'CHF'),
    ('V08', ['Oakmere Catering Ltd', 'OAKMERE CATERING LTD', 'Oakmere Catering Limited'], 'GBP'),
    ('V09', ['Vela Componentes S.A.', 'VELA COMPONENTES SA', 'Vela Componentes Sociedad Anónima'], 'EUR'),
    ('V10', ['Harbor Lane IT Services LLC', 'HARBOR LANE IT SERVICES', 'Harbor Lane IT Svcs LLC'], 'USD'),
]
BUYER = 'Tallow & Finch Studio (fictional)'
TAXID = {v[0]: 'TEST-' + v[0] + '-' + str(int(hashlib.sha256(v[0].encode()).hexdigest(), 16) % 100000).zfill(5) for v in VENDORS}
ITEMS = {
    'V01': [('A4 copy paper, box of 5 reams', 18, 32), ('Ballpoint pens, pack of 50', 6, 14), ('Desk organiser', 9, 25), ('Toner cartridge, black', 45, 95)],
    'V02': [('Pallet transport, regional', 120, 380), ('Warehouse storage, per pallet/month', 14, 30), ('Express courier surcharge', 25, 60)],
    'V03': [('Monthly office cleaning', 180, 420), ('Window cleaning, external', 60, 140), ('Consumables restock', 20, 70)],
    'V04': [('Deep clean, kitchen area', 90, 220), ('Carpet shampoo per room', 35, 80), ('Supplies', 15, 45)],
    'V05': [('Brand illustration, half day', 350, 650), ('Revisions round', 80, 160), ('Print-ready file prep', 60, 120)],
    'V06': [('Vinyl window graphic', 120, 300), ('Business cards x500', 35, 70), ('Roll-up banner', 85, 160)],
    'V07': [('Software licence, annual seat', 240, 480), ('Support plan, monthly', 90, 180), ('Onboarding session', 200, 400)],
    'V08': [('Team lunch catering, per head', 9, 18), ('Coffee service, per day', 40, 90), ('Delivery fee', 10, 25)],
    'V09': [('Aluminium bracket, unit', 2, 6), ('Fastener kit', 8, 20), ('Custom profile cut, metre', 12, 30)],
    'V10': [('Managed IT, monthly', 400, 900), ('Laptop setup, per device', 60, 120), ('On-site visit, hourly', 75, 140)],
}
TAX = {'GBP': [Decimal('20'), Decimal('0')], 'EUR': [Decimal('21'), Decimal('19'), Decimal('10')], 'USD': [Decimal('0'), Decimal('8.25')], 'CHF': [Decimal('8.1')]}
SYM = {'GBP': '£', 'EUR': '€', 'USD': '$', 'CHF': 'CHF '}

TRAP_PLAN = ([('duplicate_number', 10), ('resent_verbatim', 6), ('vat_miscalc', 12), ('mixed_tax', 8), ('foreign_currency', 10), ('decimal_ambiguity', 8),
              ('totals_mismatch', 10), ('vendor_variant', 10), ('handwritten_total', 5), ('date_ambiguity', 8), ('missing_invoice_number', 4)])

def money(x, cur, style):
    s = f'{x:,.2f}'
    if style == 'eu':
        s = s.replace(',', 'X').replace('.', ',').replace('X', '.')
    sym = SYM[cur]
    return (f'{s} {cur}' if style == 'eu' else f'{sym}{s}') if cur != 'CHF' else f'CHF {s}'

def make_invoice(i, vendor, date, traps, base=None):
    vid, names, cur = vendor
    name = names[0]
    if 'vendor_variant' in traps: name = R.choice(names[1:])
    cur_doc = cur
    if 'foreign_currency' in traps:
        cur_doc = R.choice([c for c in ('EUR', 'GBP', 'USD', 'CHF') if c != cur])
    rates = TAX.get(cur_doc, [Decimal('20')])
    rate = rates[0]
    lines = []
    for k in range(R.randint(1, 7) if base is None else 0):
        d, lo, hi = R.choice(ITEMS[vid]); qty = R.randint(1, 12) if hi < 100 else R.randint(1, 3)
        up = q(Decimal(R.uniform(lo, hi)))
        tr = rate
        if 'mixed_tax' in traps and k % 2 == 1 and len(rates) > 1: tr = rates[1]
        if 'mixed_tax' in traps and len(rates) == 1: tr = Decimal('0') if k % 2 else rate
        lines.append(dict(description=d, qty=qty, unit_price=str(up), line_net=str(q(up * qty)), tax_rate=str(tr)))
    if base: lines = base['lines']
    if 'mixed_tax' in traps and len(lines) < 2:
        d, lo, hi = ITEMS[vid][0]; up = q(Decimal(R.uniform(lo, hi)))
        lines.append(dict(description=d, qty=1, unit_price=str(up), line_net=str(up), tax_rate=str(rates[1] if len(rates) > 1 else Decimal('0'))))
    if 'decimal_ambiguity' in traps:
        while sum(Decimal(l['line_net']) for l in lines) < 1200:
            d, lo, hi = max(ITEMS[vid], key=lambda it: it[2]); up = q(Decimal(R.uniform(max(lo, 300), max(hi, 600))))
            lines.append(dict(description=d, qty=2, unit_price=str(up), line_net=str(q(up * 2)), tax_rate=str(rate)))
    net = sum(Decimal(l['line_net']) for l in lines)
    tax = sum(q(Decimal(l['line_net']) * Decimal(l['tax_rate']) / 100) for l in lines)
    gross = net + tax
    stated_net, stated_tax, stated_gross = net, tax, gross
    anomalies = []
    if 'vat_miscalc' in traps:
        stated_tax = q(tax * Decimal(R.choice(['1.1', '0.9', '1.25']))) if tax > 0 else q(net * Decimal('0.05'))
        stated_gross = stated_net + stated_tax
        anomalies.append(dict(type='vat_miscalc', field='tax_total', explanation=f'stated tax {stated_tax} != computed {tax}'))
    if 'totals_mismatch' in traps:
        stated_net = q(net + Decimal(R.choice(['10.00', '-15.50', '100.00', '0.90'])))
        stated_gross = stated_net + stated_tax
        anomalies.append(dict(type='totals_mismatch', field='net_total', explanation=f'stated net {stated_net} != sum of lines {net}'))
    hand = None
    if 'handwritten_total' in traps:
        hand = q(stated_gross - Decimal(R.choice(['50.00', '20.00', '100.00'])))
        anomalies.append(dict(type='handwritten_total', field='gross_total', explanation=f'handwritten correction {hand} over printed {stated_gross}'))
    inv_no = base['invoice_number'] if base else f'{vid}-{date.year}-{R.randint(1000, 9999)}'
    if 'missing_invoice_number' in traps:
        inv_no = None; anomalies.append(dict(type='missing_invoice_number', field='invoice_number', explanation='no invoice number on document'))
    date_style = 'long'
    if 'date_ambiguity' in traps:
        date = dt.date(date.year, R.randint(1, 9), R.randint(1, 12))
        while date.day == date.month: date = date.replace(day=R.randint(1, 12))
        date_style = 'ambiguous'; anomalies.append(dict(type='date_ambiguity', field='invoice_date', explanation='DD/MM vs MM/DD ambiguous'))
    style = 'eu' if cur_doc == 'EUR' else 'uk'   # CHF uses dot decimals (Swiss practice)
    if 'decimal_ambiguity' in traps:   # DIFFICULTY, not an anomaly: unusual separator style, totals forced >= 1,000 so the separator matters
        style = 'eu' if style == 'uk' else 'uk'
    if 'foreign_currency' in traps:
        anomalies.append(dict(type='foreign_currency', field='currency', explanation=f'{cur_doc} instead of vendor usual {cur}'))
    difficulties = [t for t in ('mixed_tax', 'decimal_ambiguity', 'vendor_variant') if t in traps]
    due = date + dt.timedelta(days=R.choice([14, 30, 45]))
    if date_style == 'ambiguous':
        while due.day > 12 or due.day == due.month: due += dt.timedelta(days=1)
    return dict(id=f'INV-{i:03d}', canonical_vendor_id=vid, vendor_name=name, vendor_tax_id=TAXID[vid],
                invoice_number=inv_no, invoice_date=date.isoformat(), due_date=due.isoformat(), buyer_name=BUYER, currency=cur_doc,
                payment_terms=f'Net {(due - date).days}', lines=lines, net_total=str(stated_net), tax_total=str(stated_tax), gross_total=str(stated_gross),
                computed=dict(net=str(net), tax=str(tax), gross=str(gross)), handwritten_total=str(hand) if hand else None,
                money_style=style, date_style=date_style, traps=sorted(traps), difficulties=difficulties, anomalies=anomalies, expected_flag=bool(anomalies))

def build():
    os.makedirs(OUT + '/invoices', exist_ok=True)
    trap_sets = [set() for _ in range(N)]
    idx = list(range(N)); R.shuffle(idx)
    trap_idx = idx[:80]
    # duplicate/resend invoices carry only that trap (16 invoices); the other 64 trap invoices share the remaining slots
    dup_slots = ['duplicate_number'] * 10 + ['resent_verbatim'] * 6
    trap_idx.sort(); dup_idx = sorted(R.sample([t for t in trap_idx if t >= 20], len(dup_slots)))
    R.shuffle(dup_slots)
    for t, k in zip(dup_slots, dup_idx): trap_sets[k].add(t)
    rest = [t for t in trap_idx if t not in dup_idx]
    slots = []
    for t, n in TRAP_PLAN:
        if t not in ('duplicate_number', 'resent_verbatim'): slots += [t] * n
    R.shuffle(slots)
    for j, t in enumerate(slots):
        k = j % len(rest)
        while t in trap_sets[rest[k]]: k = (k + 1) % len(rest)
        trap_sets[rest[k]].add(t)
    invs = []
    start = dt.date(2026, 1, 5)
    for i in range(N):
        v = VENDORS[R.randrange(len(VENDORS))]
        date = start + dt.timedelta(days=R.randint(0, 250))
        invs.append(make_invoice(i + 1, v, date, {t for t in trap_sets[i] if t not in ('duplicate_number', 'resent_verbatim')}))
    # duplicates / resends reference an earlier clean invoice of same vendor (each source used once)
    used_src = set()
    for i, ts in enumerate(trap_sets):
        if 'duplicate_number' in ts or 'resent_verbatim' in ts:
            src = R.choice([x for x in invs[:i] if not x['traps'] and x['id'] not in used_src]); used_src.add(src['id'])
            v = [vv for vv in VENDORS if vv[0] == src['canonical_vendor_id']][0]
            if 'resent_verbatim' in ts:
                dup = json.loads(json.dumps(src)); dup['id'] = invs[i]['id']; dup['traps'] = ['resent_verbatim']
                dup['anomalies'] = [dict(type='resent_verbatim', field='invoice_number', explanation=f'identical resend of {src["id"]}')]
                dup['expected_flag'] = True; dup['resend_of'] = src['id']; invs[i] = dup
            else:
                new = make_invoice(i + 1, v, dt.date.fromisoformat(src['invoice_date']) + dt.timedelta(days=R.randint(5, 40)), set())
                new['invoice_number'] = src['invoice_number']; new['traps'] = ['duplicate_number']
                new['anomalies'] = [dict(type='duplicate_number', field='invoice_number', explanation=f'same number as {src["id"]} with different amounts')]
                new['expected_flag'] = True; new['duplicate_of'] = src['id']; invs[i] = new
    # layouts / formats
    layouts = ['single', 'table', 'landscape', 'single']  # credit_note dropped in Pilot A: positive amounts under a CREDIT NOTE header would make truth ambiguous
    byid = {}
    for inv in invs:
        byid[inv['id']] = inv
        if inv.get('resend_of'):
            src = byid[inv['resend_of']]; inv['layout'] = src['layout']; inv['format'] = src['format']; continue
        inv['layout'] = R.choice(layouts) if 'handwritten_total' not in inv['traps'] else 'single'
        r = R.random()
        inv['format'] = 'clean_pdf' if r < 0.60 else 'scanned_pdf' if r < 0.85 else 'photo' if r < 0.95 else 'stamp'
        if 'handwritten_total' in inv['traps']: inv['format'] = 'scanned_pdf'
    return invs

# ---------------- rendering ----------------
def render(inv):
    land = inv['layout'] == 'landscape'
    W, H = (1754, 1240) if land else (1240, 1754)
    im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
    fb, f, fs, fm = F('inter', 40, 700), F('inter', 24, 400), F('inter', 20, 400), F('plex', 22)
    style = inv['money_style']
    def M(x): return money(Decimal(x), inv['currency'], style)
    def dstr(iso):
        y, m, dd = iso.split('-')
        if inv['date_style'] == 'ambiguous': return f'{dd}/{m}/{y}'
        return dt.date(int(y), int(m), int(dd)).strftime('%d %b %Y').lstrip('0')
    x0, y = 90, 80
    title = 'CREDIT NOTE' if inv['layout'] == 'credit_note' else 'INVOICE'
    d.text((x0, y), inv['vendor_name'], font=fb, fill='black'); y += 60
    d.text((x0, y), f"Tax ID: {inv['vendor_tax_id']}  ·  12 Fictional Street, Testville", font=fs, fill=(80, 80, 80)); y += 50
    tx = W - 520
    d.text((tx, 80), title, font=F('inter', 46, 800), fill=(30, 30, 30))
    meta = [('No.', inv['invoice_number'] or ''), ('Date', dstr(inv['invoice_date'])), ('Due', dstr(inv['due_date'])), ('Terms', inv['payment_terms'])]
    yy = 150
    for k, v in meta:
        if k == 'No.' and not v: continue
        d.text((tx, yy), f'{k}:', font=f, fill=(90, 90, 90)); d.text((tx + 120, yy), v, font=f, fill='black'); yy += 36
    y = max(y, yy) + 30
    d.text((x0, y), 'Bill to:', font=f, fill=(90, 90, 90)); d.text((x0 + 120, y), inv['buyer_name'], font=f, fill='black'); y += 70
    cols = [x0, x0 + (W - 2 * x0) * 0.50, x0 + (W - 2 * x0) * 0.60, x0 + (W - 2 * x0) * 0.74, x0 + (W - 2 * x0) * 0.86]
    if inv['layout'] in ('table', 'landscape'):
        d.rectangle([x0 - 10, y - 8, W - x0 + 10, y + 34], fill=(235, 235, 235))
    for c, h in zip(cols, ['Description', 'Qty', 'Unit', 'Tax %', 'Net']):
        d.text((c, y), h, font=F('inter', 22, 700), fill='black')
    y += 48
    for l in inv['lines']:
        d.text((cols[0], y), l['description'][:42], font=f, fill='black'); d.text((cols[1], y), str(l['qty']), font=f, fill='black')
        d.text((cols[2], y), M(l['unit_price']), font=f, fill='black'); d.text((cols[3], y), f"{Decimal(l['tax_rate']):g}%", font=f, fill='black')
        d.text((cols[4], y), M(l['line_net']), font=f, fill='black')
        if inv['layout'] == 'table': d.line([x0 - 10, y + 38, W - x0 + 10, y + 38], fill=(210, 210, 210), width=1)
        y += 46
    y += 30; tx2 = W - 600
    for k, v in [('Net total', inv['net_total']), ('Tax', inv['tax_total']), ('TOTAL DUE', inv['gross_total'])]:
        fnt = F('inter', 28, 800) if k == 'TOTAL DUE' else f
        d.text((tx2, y), k, font=fnt, fill='black'); d.text((W - x0 - 230, y), M(v), font=fnt, fill='black'); y += 46
    if inv['handwritten_total']:
        d.line([W - x0 - 235, y - 22, W - x0 + 10, y - 30], fill=(20, 40, 160), width=4)
        hf = F('inter', 34, 500)
        tmp = Image.new('RGBA', (420, 80), (0, 0, 0, 0)); ImageDraw.Draw(tmp).text((5, 5), M(inv['handwritten_total']) + '  ok', font=hf, fill=(20, 40, 160, 255))
        tmp = tmp.rotate(7, expand=True, resample=Image.BICUBIC); im.paste(tmp, (W - x0 - 330, y - 10), tmp)
    d.text((x0, H - 140), 'Payment: IBAN TEST00 0000 0000 0000 0000 (fictional) · All data in this document is fictional.', font=fs, fill=(110, 110, 110))
    if inv['format'] == 'stamp':
        st = Image.new('RGBA', (360, 120), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([4, 4, 356, 116], 14, outline=(190, 30, 40, 220), width=6); sd.text((40, 30), 'RECEIVED', font=F('inter', 50, 800), fill=(190, 30, 40, 220))
        st = st.rotate(-12, expand=True); im.paste(st, (W - 520, H // 2), st)
    # degrade
    if inv['format'] in ('scanned_pdf', 'photo'):
        im = im.convert('L').convert('RGB')
        if inv['format'] == 'photo':  # pad first so skew/perspective never crops content
            pw, ph = int(im.width * 0.08), int(im.height * 0.08); bg = Image.new('RGB', (im.width + 2 * pw, im.height + 2 * ph), (120, 110, 100)); bg.paste(im, (pw, ph)); im = bg
        ang = R.uniform(-1.6, 1.6) if inv['format'] == 'scanned_pdf' else R.uniform(-4, 4)
        im = im.rotate(ang, expand=False, fillcolor=(245, 245, 240) if inv['format'] == 'scanned_pdf' else (120, 110, 100), resample=Image.BICUBIC)
        import numpy as np
        a = np.array(im).astype('float32'); a += np.random.default_rng(len(inv['id']) * 7 + int(inv['id'][-3:])).normal(0, 9 if inv['format'] == 'scanned_pdf' else 5, a.shape)
        im = Image.fromarray(a.clip(0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(0.7))
        if inv['format'] == 'photo':
            w, h = im.size; dx = int(w * 0.04)
            im = im.transform((w, h), Image.QUAD, (dx, 0, 0, h, w, h - dx // 2, w - dx // 2, 0), resample=Image.BICUBIC, fillcolor=(120, 110, 100))
    return im

def main():
    invs = build()
    os.makedirs(OUT, exist_ok=True)
    for inv in invs:
        im = render(inv)
        fixed = dt.datetime(2026, 10, 8, 0, 0, 0).timetuple()
        im.save(f"{OUT}/invoices/{inv['id']}.pdf", 'PDF', resolution=150, creationDate=fixed, modDate=fixed, producer='HandoffTest gen_invoices.py', title=inv['id'])
    json.dump(invs, open(f'{OUT}/truth.json', 'w'), indent=1, ensure_ascii=False)
    with open(f'{OUT}/truth.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['id', 'canonical_vendor_id', 'vendor_name', 'invoice_number', 'invoice_date', 'due_date', 'currency', 'net_total', 'tax_total', 'gross_total', 'computed_gross', 'expected_flag', 'anomaly_types', 'difficulty_types'])
        for v in invs: w.writerow([v['id'], v['canonical_vendor_id'], v['vendor_name'], v['invoice_number'] or '', v['invoice_date'], v['due_date'], v['currency'], v['net_total'], v['tax_total'], v['gross_total'], v['computed']['gross'], v['expected_flag'], ';'.join(a['type'] for a in v['anomalies']), ';'.join(v.get('difficulties', []))])
    with open(f'{OUT}/manifest.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['file', 'layout', 'format', 'traps'])
        for v in invs: w.writerow([v['id'] + '.pdf', v['layout'], v['format'], ';'.join(v['traps'])])
    with open(f'{OUT}/vendors.csv', 'w', newline='') as fh:  # vendor master given to every assistant (needed to judge currency/name variants)
        w = csv.writer(fh); w.writerow(['vendor_id', 'canonical_name', 'tax_id', 'usual_currency'])
        for vid, names, cur in VENDORS: w.writerow([vid, names[0], TAXID[vid], cur])
    h = {fn: hashlib.sha256(open(f'{OUT}/{fn}', 'rb').read()).hexdigest() for fn in ['truth.json', 'truth.csv', 'manifest.csv', 'vendors.csv']}
    pdfs = {f: hashlib.sha256(open(f'{OUT}/invoices/{f}', 'rb').read()).hexdigest() for f in sorted(os.listdir(f'{OUT}/invoices'))}
    h['invoices_combined'] = hashlib.sha256(''.join(pdfs[k] for k in sorted(pdfs)).encode()).hexdigest()
    json.dump(dict(seed=SEED, n=N, generated=dt.datetime.now().isoformat(timespec='seconds'), sha256=h), open(f'{OUT}/HASHES.json', 'w'), indent=1)
    from collections import Counter
    c = Counter(t for v in invs for t in v['traps']); print('invoices', len(invs), 'flagged', sum(v['expected_flag'] for v in invs)); print(dict(c)); print(h['truth.json'][:16])

if __name__ == '__main__':
    main()
