**Inbox triage — Monday 12 October 2026, 08:30**

<row gap={2} wrap="wrap">
  <badge color="warning">12 emails requiring action today</badge>
  <badge color="danger">2 suspected phishing emails</badge>
  <badge>26 emails reviewed</badge>
</row>

The most urgent issue is **Northwind's launch**: the printer's actual deadline is Tuesday at **15:00**, not 17:00. Priya needs your feasibility answer today, potentially before 14:00. Do not wait for the 15:30 review call.

## 1. Email classification

<text color="secondary" size="xs">Priority: 1 = today · 2 = this week · 3 = optional/no action. Deadlines are action deadlines, not merely event dates.</text>

| id | category | priority | needs reply | one-line summary | action for me | deadline |
|---|---|---|---|---|---|---|
| 1 | client_urgent | **1** | yes | Northwind launch moved to Wed 14 Oct; boards needed Tuesday. | Check capacity and confirm feasibility to Priya today, before 14:00; use actual 15:00 printer cutoff. | 2026-10-12 |
| 2 | newsletter_promo | 3 | no | Design newsletter with font ideas and webinar promotions. | none | none |
| 3 | admin_finance | **1** | yes | £2,572.35 invoice overdue since 25 May. | Verify invoice V06-2026-1298 and payment status; pay if valid/unpaid or explain issue to supplier. | 2026-05-25 |
| 4 | task_internal | **1** | no | Tom is sick today; Harbor Lane logo 90% complete. | Arrange coverage and assign someone to finish/check logo files. | 2026-10-12 |
| 5 | client_question | 2 | yes | Harbor Lane wants a one-colour logo suitable for invoices. | Confirm feasibility and incorporate a monochrome version. | 2026-10-31 |
| 6 | newsletter_promo | 3 | no | Office supplies 40% promotional discount, ending Tuesday. | none | none |
| 7 | suspicious | **1** | no | Likely phishing: fake Microsoft warning and password-verification URL. | Do not click; report phishing and block sender. | none |
| 8 | proposal | 2 | yes | Nordhaven requests scope and price range for 2027 brand refresh. | Prepare proposal covering logo, website and packaging. | 2026-10-23 |
| 9 | meeting | **1** | no | Studio stand-up 11:00; Northwind review 15:30. | Attend both; resolve Northwind feasibility before review. | 2026-10-12 |
| 10 | client_question | 3 | no | Marco disputed €1,800 brochure quote versus €1,600. | none — superseded by email 26. | none |
| 11 | notification | 3 | no | September bank statement available online. | none | none |
| 12 | task_internal | 2 | yes | Ava requests annual leave from 26–30 October. | Check staffing and approve/decline leave. | none |
| 13 | admin_finance | **1** | yes | Atelier Mirelle requires signed copyright transfer before second-invoice payment. | Retrieve 2 Oct attachment, review terms, sign if appropriate and send back. | none |
| 14 | newsletter_promo | 3 | no | Promotional profile-search notification. | none | none |
| 15 | supplier | 2 | yes | Caterer needs final headcount and dietary requirements for 22 Oct lunch. | Collect details and send final numbers. | 2026-10-16 |
| 16 | newsletter_promo | 3 | no | Vela Componentes 2027 catalogue announcement. | none | none |
| 17 | client_urgent | **1** | no | Northwind requests larger prices and sourdough photo instead of croissant. | Apply changes and deliver final print-ready boards by revised cutoff. | 2026-10-13 |
| 18 | admin_finance | 3 | no | Two-seat software licence renews automatically for CHF 892.50 on 1 Nov. | none unless changing seat count. | none |
| 19 | supplier | **1** | yes | Jonas offers shoot on Thu 15 or Fri 16; needs decision by Tuesday. | Confirm whether shoot is still required after launch; select date with Jonas if needed. | 2026-10-13 |
| 20 | notification | 3 | no | Business-rates direct debit active; £214 first collection on 1 Nov. | none | none |
| 21 | newsletter_promo | 3 | no | Optional AI webinar starts today at 10:30. | none | none |
| 22 | meeting | **1** | yes | Dana requests moving Harbor Lane review from Thu 15 to Fri 16 at 10:00. | Check availability and accept or suggest another time. | 2026-10-15 |
| 23 | suspicious | **1** | no | Suspicious £1.99 parcel redelivery-fee request. | Do not pay or click; report and verify deliveries independently if concerned. | none |
| 24 | task_internal | **1** | no | Ava reports Northwind printer cutoff is Tuesday 15:00, two hours earlier. | Verify cutoff with printer and immediately inform Priya/team. | 2026-10-13 |
| 25 | notification | 3 | no | Brightwell order #4471 (paper and toner) ships, expected Tuesday. | none | none |
| 26 | client_question | 3 | no | Marco confirms €1,800 quote is correct and says approval will follow today. | none — wait for actual approval. | none |

## 2. Today's to-do list — in recommended order

{@body const todos = [
{time:"08:30 — Immediately",title:"Resolve Northwind production feasibility",detail:"Contact Ava/the printer, confirm the Tuesday 15:00 cutoff, check who can finish the boards, and inform Priya. Give her a yes/no answer before 14:00; ideally much earlier.",ids:"1, 17, 24"},
{time:"Early morning",title:"Assign final Northwind artwork",detail:"Increase menu prices, replace the croissant photo with sourdough, check print specifications and arrange final quality control.",ids:"17"},
{time:"Early morning",title:"Cover Tom's absence",detail:"Ask someone to take over Harbor Lane's 90%-complete logo files, including the one-colour variant. Check readiness for the proposed Friday review.",ids:"4, 5"},
{time:"Before meetings",title:"Respond to Dana and coordinate Jonas",detail:"Check whether Friday 16 October at 10:00 works for Harbor Lane. Ask Priya whether a product shoot on 15/16 October remains useful after Wednesday's launch before committing Jonas.",ids:"19, 22"},
{time:"11:00–11:15",title:"Attend studio stand-up",detail:"Confirm ownership of Northwind production and Harbor Lane coverage.",ids:"9"},
{time:"Today",title:"Unblock Atelier Mirelle's invoice",detail:"Locate the copyright transfer from 2 October and review its scope before signing. Return it if acceptable so the second invoice can be paid.",ids:"13"},
{time:"Today",title:"Investigate Kestrel overdue invoice",detail:"Check accounts for payment against V06-2026-1298. Arrange verified payment or respond with the discrepancy.",ids:"3"},
{time:"Today",title:"Report two suspected phishing messages",detail:"Report the fake Microsoft security threat and parcel redelivery-fee message. Don't open the supplied links.",ids:"7, 23"},
{time:"15:30–16:00",title:"Attend Northwind review call",detail:"Review progress with Priya and confirm the final printer handoff arrangements. This call is too late for the earlier 14:00 decision requirement.",ids:"9"},
{time:"End-of-day check",title:"Check Casa Albarel approval",detail:"Marco withdrew the price objection and expects to approve the €1,800 quote today. No reply is needed unless approval fails to arrive and follow-up becomes useful.",ids:"10, 26"}
]}
{@body const [done,setDone] = DIL.useState([])}
<box border radius="xl" padding={3} gap={3}>
  <row align="center" justify="between">
    <text weight="medium">Today's checklist</text>
    <text color="secondary" size="xs" tabularNums>{done.length} / {todos.length} completed</text>
  </row>
  <box background="surface-tertiary" height="6px" radius="full" clip>
    <box background="surface-inverted" height="100%" width={`${100*done.length/todos.length}%`} radius="full"/>
  </box>
  {#each todos as item,i}
    <box key={i} gap={1}>
      <checkbox checked={done.includes(i)} onChange={v=>setDone(p=>v?[...p,i]:p.filter(x=>x!==i))} lineThrough={false}>
        <box gap="2px">
          <text color="secondary" size="xs">{item.time}</text>
          <text weight="medium" lineThrough={done.includes(i)}>{item.title}</text>
          <text size="sm" color="secondary">{item.detail}</text>
          <caption>Emails {item.ids}</caption>
        </box>
      </checkbox>
      {#if i!==todos.length-1}<divider color="subtle"/>{/if}
    </box>
  {/each}
</box>

## 3. Conflicts and easily missed details

<box gap={3}>
  <row align="start" gap={2}>
    <icon name="alert-triangle" color="danger" size="lg"/>
    <box flex="1" gap={1}>
      **Northwind: printer deadline contradiction**

      Email 1 says Tuesday 17:00, but email 24 says the printer stops accepting files at **15:00 on Tuesday 13 October**. Treat 15:00 as the operational cutoff, subject to direct confirmation. Wednesday's launch cannot rely on Friday's original timeline.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="clock" color="warning" size="lg"/>
    <box flex="1" gap={1}>
      **The Northwind review call is too late**

      Priya needs to know by 14:00 if the job is not feasible. The review starts at 15:30. Email or call her beforehand.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="calendar-x" color="warning" size="lg"/>
    <box flex="1" gap={1}>
      **Northwind product photography happens after launch**

      Jonas is available 15/16 October, but the launch is now Wednesday 14 October. These photos cannot support launch-day materials unless the timing changes. Friday's shoot may also conflict with Dana's proposed 10:00 review; no shoot time is confirmed.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="file-signature" color="secondary" size="lg"/>
    <box flex="1" gap={1}>
      **Atelier Mirelle: payment dependency is buried**

      The copyright form is not attached to email 13; it's in the email from **2 October**. Review the legal terms before signing. Payment of the second invoice depends on it.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="check-check" color="success" size="lg"/>
    <box flex="1" gap={1}>
      **Casa Albarel: price dispute resolved**

      Email 26 cancels the concern from email 10. The €1,800 quotation is correct, but approval is only promised, not confirmed.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="shield-alert" color="danger" size="lg"/>
    <box flex="1" gap={1}>
      **Two potential scams**

      Email 7 impersonates Microsoft using `m1crosoft` with a digit 1 and a password-verification URL. Email 23 requests a redelivery payment through a separate domain and provides no order reference. Do not use either link. Email 25's genuine-looking shipment notice does not validate the payment request.
    </box>
  </row>
  <divider color="subtle"/>
  <row align="start" gap={2}>
    <icon name="calendar-days" color="secondary" size="lg"/>
    <box flex="1" gap={1}>
      **Upcoming dates worth tracking**

      13 Oct: print handoff and Jonas decision. 16 Oct: catering headcount. 22 Oct: studio lunch. 23 Oct: Nordhaven proposal. 26–30 Oct: Ava's requested leave, not yet approved. 31 Oct: Harbor Lane one-colour logo request. 1 Nov: software auto-renewal and first business-rates debit.
    </box>
  </row>
</box>

**Bottom line:** Prioritise the Northwind production deadline, arrange cover for Tom, and clear the two payment-related issues. The other time-sensitive responses can be handled around the scheduled meetings.