# Blueprint No. 04: AI sales system

Source: https://restructure-europe.vercel.app/en/newsletter/sales/ (loaded OK). The page text is short. Department and agent names come from the map image (`sales-map.jpg`, titled "How an AI sales system makes an extra EUR 20K/month for your business"). The map is low resolution, so some small labels and logos are best-effort readings.

## Purpose and audience
B2B and high-ticket service SMBs. Find in-market buyers, contact inbound leads in under 60 seconds, nurture them, and hand closers to humans.

## Structure (map)
- **Inputs**: signals (website visits, buying signals, forms and calls, replies, messages and meetings, deals and payments), a system of record (leads and deals, contacts, meetings, playbooks and files), and partner/owner input (the setup, offer and targets, voice and languages, approvals). There is also a Sales DB.
- **Brain, "Sales Command Center"**: takes your brief, routes the work, decides who is hot, guards the gate. Every morning ends in one page.
- **What interrupts the loop** (event handlers): form filled at 11pm; "not right now"; "stop emailing me"; buyer back on the pricing page; meeting no-show; buyer asks for a discount; hot buyer wants a human; new country, new language.
- **Knowledge layer**: markdown files. Partially legible: profile, customer, signals, rubric, offer, stories, messages, a DE-FR-NL file, and consent/GDPR-related files.

## Departments and agents (map; about 5 per department)
| Department | Agents | Trigger | Output |
|---|---|---|---|
| Market & ICP Intel | ICP Builder, Market Mapper, Competitor Watcher, Offer Builder, Weekly Market Brief | Weekly | ICP and positioning |
| Buyer Intent Engine | Website Visitor ID, Hiring Signal, Funding & News Signal, Intent Scorer, Hot List | Every morning | Ranked hot list. Jev scores in seconds |
| Personalized Outreach | Message Writer, Translator, Email Sender, LinkedIn Sender, Reply Sorter | Hot list | Outbound messages in the buyer's language |
| Speed-to-Lead Engine | Form Catcher, 60-Second Caller, Question Answerer, Meeting Booker, Show-Up Reminder | Form submission | ElevenLabs voice call in under 60s in the lead's language; meeting booked on the call |
| Pipeline Nurture Engine | Follow-Up Planner, Multi-Channel Sender, Objection Finder, Proof Sender, Re-Engager | No yes yet | Day 2/5/10 follow-ups. Adapts to the objection |
| Deal Desk | Meeting Prep, Call Notes, Proposal Writer, Contract & Payment, Win/Loss Reviewer | Meeting booked / deal stage | Proposals, contracts, payments, post-mortems |
| Sales Command Center | Router, Human Handoff, Approval Gate, **GDPR Guard**, Morning Brief | All | Handoffs and the daily page |

**Data and observability panels**: Pipeline, Outreach, Speed to lead, Meetings & revenue, Agent activity. **Human handoff**: You (approvals), your sales team, your buyers.

## Tools (text: ElevenLabs, Jev; others from map logos)
Claude, ElevenLabs (voice agent), Jev, n8n, Pipedrive, Cal.com, Stripe, Slack, Notion, Gmail. Also LinkedIn and an enrichment/visitor-ID tool whose logo is unclear.

## Human approval gates
- An Approval Gate and Human Handoff in the command center.
- "Hot buyer wants a human" triggers a handoff.
- Discount requests are an interrupt event. The approver is presumably the owner, but the page does not say.
- No thresholds are given.

## Data / memory
- Markdown knowledge layer (profile, ICP rubric, offer, stories, message templates, per-language files).
- A Sales DB.

## Reports and KPIs
- Every morning, one page: meetings booked, deals about to close, incoming money.
- The map's terminal mock shows "42 hot buyers ranked; 18 calls, 47s avg; 3 proposals; one page sent 7:00".
- KPIs: speed-to-lead seconds, meetings booked, show rate, pipeline value.

## Claims (theirs)
- "Extra EUR 20,000 a month".
- Call-back in under 60 seconds.
- "Always the first one they talk to".

## Gaps for a builder
- **Outbound AI voice calls**: consent to be called and AI disclosure are needed. In the EU, ePrivacy and national rules apply (e.g. Germany requires prior consent for B2C calls and presumed consent for B2B). In the US, TCPA rules apply and the FCC treats AI voices as "artificial voice". Only a "GDPR Guard" box is shown, with no logic.
- Website visitor identification (reverse IP / person-level) has GDPR/ePrivacy cookie-consent implications.
- LinkedIn automation violates LinkedIn's terms of service.
- No agent count, cost per call, or fallback when the voice agent fails.
- Opt-out handling: "stop emailing me" exists as an event, but there is no suppression-list design.
