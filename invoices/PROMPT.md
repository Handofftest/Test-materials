You are processing supplier invoices for a small business. All documents are fictional test data.

You will receive two PDFs: HandoffTest_Part1_p001-100.pdf (100 pages) and HandoffTest_Part2_p101-200.pdf (100 pages). Each page is exactly one invoice. In each message I will name one file and a range of 10 pages. Process ONLY those 10 pages.

Vendor master list (vendor_id | canonical_name | tax_id | usual_currency):
V01 | Brightwell Office Supply Ltd | TEST-V01-46902 | GBP
V02 | Nordhaven Logistik GmbH | TEST-V02-58370 | EUR
V03 | Casa Albarel S.L. | TEST-V03-11587 | EUR
V04 | Pinecrest Cleaning Co. | TEST-V04-73428 | USD
V05 | Atelier Mirelle SARL | TEST-V05-67798 | EUR
V06 | Kestrel Print & Signage | TEST-V06-35089 | GBP
V07 | Zurlinden Software AG | TEST-V07-75369 | CHF
V08 | Oakmere Catering Ltd | TEST-V08-69274 | GBP
V09 | Vela Componentes S.A. | TEST-V09-41086 | EUR
V10 | Harbor Lane IT Services LLC | TEST-V10-23457 | USD

For EACH page in the named range, return one JSON object. Return the 10 objects as a single JSON array and nothing else.

Schema (use exactly these keys):
{
  "file": "<part and page number within that file, e.g. Part1 p3>",
  "vendor_id": "<vendor_id from the master list, or \"unknown\">",
  "vendor_name_as_printed": "<string>",
  "vendor_tax_id": "<string or \"unknown\">",
  "invoice_number": "<string, or \"unknown\" if none is printed>",
  "invoice_date": "<YYYY-MM-DD, or \"unknown\" if it cannot be determined with certainty>",
  "due_date": "<YYYY-MM-DD, or \"unknown\">",
  "currency": "<ISO code: EUR, GBP, USD, CHF>",
  "net_total": "<number with 2 decimals, as printed on the document>",
  "tax_total": "<number with 2 decimals, as printed>",
  "gross_total": "<number with 2 decimals, as printed (the printed TOTAL DUE)>",
  "anomalies": [ { "type": "<one of the types below>", "explanation": "<short>" } ]
}

Allowed anomaly types (use only these; return [] if none apply):
- duplicate_number: same vendor and invoice number as another invoice in this range or in an earlier range in this conversation, with different amounts
- resent_verbatim: an identical copy of another invoice already seen
- vat_miscalc: printed tax total does not equal the line nets x their tax rates
- totals_mismatch: printed net total does not equal the sum of the line nets
- handwritten_total: a handwritten or manual correction changes the amount to pay
- foreign_currency: currency differs from the vendor's usual_currency in the master list
- date_ambiguity: the invoice date cannot be read unambiguously (e.g. 03/04/2026)
- missing_invoice_number: no invoice number printed

Rules:
- Do not guess. If a value cannot be read with certainty, write "unknown".
- Amounts: write numbers with a dot as the decimal separator and no thousands separators (e.g. 1234.56).
- Report amounts exactly as printed, even if they are wrong; report the error as an anomaly.
- Keep page order.
