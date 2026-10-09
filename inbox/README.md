# Inbox: sort your email with ChatGPT (prompt included)

## The test
- We wrote a fictional inbox of 26 emails. It hides 5 traps:
  - a fake Microsoft security warning
  - a parcel-fee scam
  - a question that the sender cancelled in a later email
  - a "sign this form before we can pay you" task buried in a long thread
  - a printer deadline that quietly moved from 5pm to 3pm
- We pasted the inbox into a normal ChatGPT chat: ChatGPT Plus, GPT-6 Thinking (High), with no plugins and no connection to a real mailbox.

## Files
| File | What it is |
|---|---|
| `inbox.txt` | The 26 fictional emails (`.example` addresses) |
| `prompt_1_triage.md` | Prompt for the triage table: run 1, no priority rule |
| `prompt_1b_triage_with_rule.md` | The same prompt plus our priority-1 rule (run 2). **Start with this one.** |
| `prompt_2_drafts.md` | Follow-up prompt for reply drafts |
| `answer_key.json` | Our answer key, written before the run |
| `score_inbox.py` | Marks a triage table against the answer key |
| `results/` | ChatGPT's answers, unedited |

## Step by step
1. **Pick a small batch of emails.** Copy them into the chat as plain text. Leave out passwords, bank details, health information and anything confidential. Check your company's rules first.
2. **Paste the table prompt** from `prompt_1b_triage_with_rule.md`. Change the date and time on the first line.
3. **Write your own priority-1 rule.** This is the step that made the difference. Ours is in the next section.
4. **Read the table and today's list.** Check the "conflicts or easy to miss" section at the end.
5. **Ask for drafts** with `prompt_2_drafts.md`. Everything you haven't decided goes in [square brackets].
6. **Read every draft before you send it.** You fill in the brackets, you decide, you send. Nothing here is automatic.

## The priority rule we used
> My rule for priority 1: only if something is due today or tomorrow, a client or a teammate is blocked waiting for me, or money is at risk today. Scams and phishing are priority 3. Calendar reminders are priority 3.

Write your own version. The AI doesn't know what "urgent" means to you until you tell it.

## Our results (9 Oct 2026)
- **Run 1, no rule:**
  - The table took 1 min 46 s.
  - Categories matched our key on 22 of 26 emails. Deadlines were right on 7 of 8.
  - All 5 traps were caught.
  - **Too many urgent emails:** 11 of 26 were marked "deal with today", including both scams and a calendar reminder. Our key had 4.
- **Run 2, fresh chat with the rule:**
  - 5 emails were marked "today", and all traps were still caught.
  - Where it disagreed with us, it was a judgement call. It moved a colleague's sick-day email to "this week" and made the photographer priority 1, because his deadline was the next day.
- **Drafts:**
  - 9 replies in 73 seconds, with undecided points in brackets.
  - One draft added a promise the sender never made: "I'll get back to you by Tuesday." That's why you read every draft.

Mark your own table:
```
python3 score_inbox.py my_table.md
```
Your table must use the same columns as the prompt. The script reports category, priority, reply and deadline accuracy against `answer_key.json`.

## Limits
- One tool, one fictional inbox of 26 emails, two runs. Real inboxes are messier.
- We didn't time the same work by hand, so we make no time-saving claims.
- AI drafts can add facts or promises you didn't make. Never send without reading.
