# Blueprint No. 10: AI financial operating system

Source: https://restructure-europe.vercel.app/en/newsletter/financial-os/ (loaded OK). Module names and tools also come from the map image. (logo) means the tool was identified from an icon.

## Purpose and audience
Background accounts-receivable automation for service SMBs. It goes contract to invoice to chase to weekly cash view, so the owner gets paid faster.

## Departments / modules (map: "35 AI finance agents, in the background", 7 modules x 5)
| Module | Agents | Trigger | Inputs | Outputs |
|---|---|---|---|---|
| Deal Intake | 5 | Contract signed | Signed contract. E-signature tool (logo: "D" mark, likely Documenso, DocuSign or Dropbox Sign; unconfirmed) and HubSpot (logo) | Client, price and terms extracted |
| Invoice Engine | 5 | Same minute the contract is signed | Signed-contract email in Gmail | Invoice built in QuickBooks. Claude drafts the cover email, and the **owner checks and sends it** |
| Payment Chaser | 5 | Invoice past due | Payment status | Automatic polite reminder, then a second reminder a few days later. If still unpaid after **2 weeks**, Jev escalates to the owner. WhatsApp Business (logo) is a channel |
| Cash Brief | 5 | Every Friday | Bank and ledger data. Google Sheets and Wise (logo) | One page: money in, money out, cash balance, who owes what |
| Payments | 5 | Payment events | Stripe and a second payments icon (unidentified) | Reconciliation of received payments |
| Expenses | 5 | Receipts and bills | Dext and Bill.com (logo) | Captured expenses |
| Finance Brain | Orchestrator | All events | Gmail, QuickBooks and Stripe | Learns each client's payment behaviour (always on time vs needs a nudge) |
| Knowledge | none | n/a | Notion and Google Drive (logo) | n/a |
| You + Approvals | none | n/a | Slack and Telegram (logo) | Approvals and alerts |

## Tools
Claude, Jev, Gmail, QuickBooks, Stripe, HubSpot, e-sign tool (D logo), WhatsApp Business, Google Sheets, Wise, Dext, Bill.com, Notion, Google Drive, Slack, Telegram.

## Human approval gates
- Every invoice email: Claude drafts it, and the human reviews and hits send.
- Escalation at 14 days unpaid goes to the human, who makes the call.
- The map has a "You + Approvals" node in Slack/Telegram. No monetary thresholds are given.

## Data / memory
- Per-client payment-behaviour profile maintained by the brain.
- Knowledge store in Notion/Drive.

## Reports and KPIs
- **Friday cash brief**: inflows, outflows, cash on hand, outstanding receivables by client.
- Implied KPIs: time from contract to invoice, days sales outstanding, overdue count.

## Claims (theirs)
- Invoices go out "the same minute the deal closes", so money arrives days sooner.
- "Gets smarter every week".
- 35 agents.

## Gaps for a builder
- VAT/IVA handling, e-invoicing mandates (e.g. Italy SdI, France 2026+, Germany XRechnung/ZUGFeRD, Poland KSeF) and invoice numbering rules are absent. These are critical in the EU.
- How contract terms are parsed when the contract is a PDF attachment or comes from an e-sign platform rather than Gmail.
- The reminder cadence (only "a few days" between reminders), tone escalation, late-payment interest (EU Late Payment Directive) and stopping on dispute are not specified.
- How Stripe payouts are matched against QuickBooks invoices.
- The roles of the Expenses and Payments modules are not described in the text.
- Access control and audit trail for the finance data.
