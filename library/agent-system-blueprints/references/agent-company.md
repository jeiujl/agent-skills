# Blueprint No. 08: AI company system ("137 agents")

Source: https://restructure-europe.vercel.app/en/newsletter/agent-company/ (loaded OK, includes "How it's built" detail). The map image alt text lists the layers: signals, system of record, owner input, company brain, knowledge layer, "what interrupts the loop", 7 departments, data and observability, human handoff.

## Purpose and audience
A whole-company agent architecture for B2B or service SMBs. Seven departments share one "company brain".

## Departments (map lists 7: Sales, Deals, Marketing, Back Office, Operations, Intelligence, Customer)
The page details four of them plus the brain.

**Sales.** Triggers: a daily morning run, and form submissions.
- Buyer Intent Scout: Dealfront identifies companies visiting the pricing page, and Jev ranks them.
- 60-Second Caller: calls back in under 60 seconds after a form fill, using ElevenLabs Agents and Twilio.
- Meeting Booker: books in Cal.com and saves the lead to HubSpot.
- Follow-Up Engine: Claude follows up on day 2, 5 and 10.

**Marketing.** Trigger: a closed deal, which signals who to target next.
- Audience Mapper: SparkToro.
- Video Ad Maker: Higgsfield and ElevenLabs.
- Campaign Builder: Meta Ads and Google Ads.
- Budget Mover: Jev shifts budget toward revenue.
- Gate: **nothing goes out without owner approval.**

**Operations.** Trigger: a contract signed in Deals.
- Project Setup: Asana via n8n.
- Kickoff Builder: Claude writes the kickoff doc, booked in Cal.com.
- Deadline Watcher: Jev flags late work in Slack.
- Invoice Trigger: invoices via Stripe when the job is done.

**Intelligence.** Produces the Monday page.
- Data Puller: Supermetrics into BigQuery.
- Ad-to-Revenue Matcher: links ad, then lead, then deal, then payment.
- Churn Predictor: Jev.
- Monday Page agent: Claude writes it and sets next-week priorities in Notion.

**Company brain.** Every department reads from it and reports back.
- Claude writes and decides.
- Claude Code builds the workflows.
- Jev makes "millisecond" decisions.
- n8n moves work between departments.
- Notion and Google Drive hold prices, clients, processes and files.
- LangSmith and Langfuse provide observability: per-agent cost and errors.
- The owner sets targets and limits once.

## Tools
Claude, Claude Code, Jev, n8n, Dealfront, ElevenLabs Agents, Twilio, Cal.com, HubSpot, SparkToro, Higgsfield, Meta Ads, Google Ads, Asana, Slack, Stripe, Supermetrics, BigQuery, Notion, Google Drive, LangSmith, Langfuse.

## Human approval gates
- Marketing output requires approval.
- Owner-set targets and limits.
- A "human handoff" layer to you, your team and your customers (map).
- No specific thresholds are given.

## Data / memory
- The company brain (Notion and Drive): prices, clients, processes.
- Shared state means "when sales closes, operations already knows".

## Reports and KPIs
- **Monday page**: where revenue came from, what is at risk (churn), and next actions.
- KPIs: ad-to-revenue attribution, churn risk, late tasks, speed-to-lead.

## Claims (theirs)
- 137 agents.
- "More revenue every single month".
- Call-back in under 60 seconds.

## Gaps for a builder
- Only 4 of the 7 departments are described. Deals, Back Office and Customer are missing.
- No breakdown of the 137 agents.
- Dealfront visitor de-anonymisation and the outbound AI call under GDPR/ePrivacy: lawful basis, consent and AI disclosure are not addressed.
- No error handling or escalation policy, and no permission model.
- No cost model for LangSmith/Langfuse, BigQuery and voice minutes.
- "Jev" is undefined.
