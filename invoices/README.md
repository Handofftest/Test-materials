# Invoices: 200 synthetic invoices, 65 hidden problems

## The test
- We gave each assistant the same 200 fictional supplier invoices, split into two 100-page PDFs.
- Every assistant got the same instructions, word for word.
- The task: extract 8 fields from every invoice and flag anything an accounts clerk should stop and check.
- A script marked each answer against an answer key we wrote before any assistant saw the files.

## Files
| Path | What it is |
|---|---|
| `pdf/HandoffTest_Part1_p001-100.pdf`, `pdf/HandoffTest_Part2_p101-200.pdf` | The exact two files every assistant received. Image-only PDFs: no text layer and no hidden answers. |
| `dataset/vendors.csv` | The supplier list given to every assistant (also embedded in the prompt) |
| `dataset/truth.json`, `dataset/truth.csv` | The answer key: correct fields and planted problems for every invoice |
| `dataset/manifest.csv` | Format, layout and trap type for each invoice |
| `batches/batch_map.csv` | Which invoice is on which page |
| `PROMPT.md` | The instructions sent in message 1 |
| `MESSAGES.txt` | All 20 messages (10 pages each), in order |
| `score.py` | The marking script |
| `gen_invoices.py` | The generator that rebuilds the dataset from a seed |
| `results/chatgpt_outputs.json`, `results/claude_outputs.json` | The assistants' answers, unedited |

SHA-256 of the files the assistants received:
- Part 1: `af8d3cac439f98e8e812dde9e2792642712e72d57728cfbe21160c366dcb8db0`
- Part 2: `b490654772d850585eafaacedd266159a666c4e308bcd1090f604b470845014d`
- `truth.json`: `92fba05b5d53a90feb87b108fea1d41d645a61b29737d71bf2eb7a828ee838fd`

## What's in the dataset
- 200 invoices from 10 fictional suppliers, in EUR, GBP, USD and CHF.
- Formats:
  - 118 clean PDFs
  - 51 crooked scans
  - 23 phone photos
  - 8 stamped invoices
- 65 planted problems across 63 invoices:

| Problem | Count |
|---|---|
| Tax miscalculated | 12 |
| Net total doesn't match the lines | 10 |
| Unusual currency for that supplier | 10 |
| Same invoice number, different amount | 10 |
| Ambiguous date (DD/MM vs MM/DD) | 8 |
| Same invoice sent twice | 6 |
| Handwritten correction to the total | 5 |
| Missing invoice number | 4 |

- 17 more invoices carry "difficulties" that are *not* errors and must not be flagged: a supplier name variant, two VAT rates on one invoice, or an unusual decimal style.

## Method
1. Start a new chat and attach both PDFs.
2. Send message 01 from `MESSAGES.txt` (it contains the full prompt), then messages 02–20 one by one, waiting for each answer.
3. Keep everything in one conversation, so the assistant can spot duplicates across batches.
4. Don't correct the answers. One retry is allowed, only if the app itself fails.
5. Save each reply. Combine all the JSON arrays into one file, for example `my_outputs.json`.
6. Mark it:
   ```
   python3 score.py my_outputs.json --label my_test
   ```
   The scores are written to `results/my_test/`: `score.json`, `per_invoice.csv` and `errors.csv`.

### Marking rules (fixed before any run)
- **Fields scored:** vendor_id, invoice_number, invoice_date, due_date, currency, net_total, tax_total, gross_total.
- **Amounts:** compared to the cent.
- **Ambiguous dates:** "unknown" or the true date both count as correct.
- **Missing invoice numbers:** "unknown" counts as correct.
- **Problems:** scored per invoice and problem type. A flag with the wrong type is a false alarm.
- **Critical error:** a wrong supplier, currency or total due, or a missed duplicate, resend or handwritten correction.

### Rebuild the dataset
```
pip install pillow
# put Google Fonts (OFL) folders inter/, jetbrainsmono/, manrope/, dmsans/, ibmplexmono/ in ./fonts or set FONTS_DIR
python3 gen_invoices.py 20261008 200
```
- The generator writes `dataset/invoices/INV-###.pdf` plus the answer key.
- To rebuild the two test files, merge the invoices in the page order of `batches/batch_map.csv` with any PDF tool, for example `qpdf --empty --pages ... -- out.pdf`.
- A different seed gives you a fresh, unseen test set.

## Our results (one run each, 9 Oct 2026)

| | Claude · Max · Opus 5.5 (high) | ChatGPT · Plus · GPT-6 Thinking (high) | Gemini · free · 3.1 Pro |
|---|---|---|---|
| Fields correct | 1,600 / 1,600 | 1,597 / 1,600 | did not complete |
| Problems found | 65 / 65 | 63 / 65 | – |
| False alarms | 0 | 1 | – |
| Total response time | 13 min 28 s | 36 min 14 s | – |

### What went wrong
- **ChatGPT misread three invoice numbers:**
  - INV-045: 9858 read as 8958
  - INV-091: 8165 read as 8155
  - INV-106: 9292 read as 9282
- **ChatGPT missed a €100 gap.** Part 1, page 33: the printed net total is €100 more than the lines. It copied the amounts correctly but raised no flag.
- **ChatGPT gave the wrong reason for a £10 gap.** Part 2, page 25: the net total is £10 more than the line. It reported a tax error instead.
- **Gemini (free plan) did not finish.** It returned "Sorry, something went wrong." on the first try and "I encountered an error doing what you asked." on the retry.
  - The mode selector showed Gemini Pro (3.1 Pro) when we sent the task. After the retry it showed "Flash Avanzado", a change the app made, not us.
  - The app gave no reason. The free plan's smaller context window is a possible cause, not a confirmed one.
  - Gemini is unscored, which is not the same as 0%.
- **Timing:** measured from clicking Send to the end of each answer, using each service's own message timestamps.

These are different plans (Max, Plus and free) and one run each. This is not a general ranking of the models.

## Before you use AI on real invoices
- Use a fixed list of fields and one output format.
- Give it your supplier list.
- Tell it not to guess: "unknown" is an allowed answer.
- Ask it to check the maths and look for duplicates, and to explain every flag.
- Work in small batches, all in one conversation.
- Check the totals yourself: lines + tax = total due.
- Don't pay anything just because an AI said so. Check your company's rules before you upload real documents.
