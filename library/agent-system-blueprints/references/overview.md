# ReStructure AI Europe: 11 blueprints overview

All 11 pages loaded (HTTP 200, 10 Nov 2026). Source: the public blueprint pages of ReStructure AI Europe (re-structure.ai/eu/en/newsletter), summarised in our own words. Several pages have thin prose, so their structure was read from the public map images on each page. Agent counts and money figures are the company's own claims.

## Summary table
| # | Blueprint | Agents claimed | Core modules | Key tools |
|---|---|---|---|---|
| 11 | Market research | 35 (7x5) | Competitor Intel, Customer Voice, Demand Radar, Translation, Price Tracker, Social Listening, Research Brain, Monday page | Claude, Jev, Google Maps, Apify, Trustpilot, Reddit, Google Trends, DeepL, Semrush |
| 10 | Financial OS | 35 (7x5) | Deal Intake, Invoice Engine, Payment Chaser, Cash Brief, Payments, Expenses, Finance Brain | Claude, Jev, Gmail, QuickBooks, Stripe, HubSpot, Wise, Dext, Bill.com, Slack/Telegram |
| 09 | Ad agency | 35 | Strategist, Creative Studio, Performance Monitor, Ads Brain, Monday page | Claude, Jev, n8n, Higgsfield, CapCut, ElevenLabs, Descript, Meta/TikTok/Google Ads, HubSpot, CallRail, Stripe, Airtable, Notion |
| 08 | Company system | 137 | 7 departments (Sales, Deals, Marketing, Back Office, Operations, Intelligence, Customer) plus company brain | Claude, Claude Code, Jev, n8n, Dealfront, ElevenLabs Agents, Twilio, Cal.com, HubSpot, SparkToro, Asana, Supermetrics, BigQuery, LangSmith, Langfuse |
| 07 | One-person marketing team | 36 ("23 employees") | Research and content, Creative and distribution, Analytics loop, Email and nurture, Leads and booking, Search and website, morning page | Claude Code, Jev, n8n, Higgsfield, ElevenLabs, Metricool, ManyChat, Beehiiv, Calendly, HubSpot, Stripe, Looker Studio |
| 06 | AI social media team | not stated | Content Studio, Publishing, Comments to customers, morning page | Claude Code, Apify, Airtable, Higgsfield, ElevenLabs (voice clone/dub), Canva, Buffer, ManyChat, DeepL, Stripe links, Calendly |
| 05 | Shopify store | 41 (8 departments) | Ad Studio, 3 Languages, Paid Ads, Cart Recovery, Repeat Buyers, Support, Profit Guard, Morning page | Shopify, Klaviyo, WhatsApp Business, Usercentrics, Gorgias, AfterShip, Loop Returns, Triple Whale, DeepL, Higgsfield |
| 04 | Sales system | not stated (about 35 on map) | Market & ICP Intel, Buyer Intent, Personalized Outreach, Speed-to-Lead, Pipeline Nurture, Deal Desk, Command Center | ElevenLabs voice, Jev, Claude, Pipedrive, Cal.com, Stripe, LinkedIn |
| 03 | Claude CMO marketing system | 35 (6 teams) | Market Intel, Ad Factory, Launch, Speed-to-Lead, Money Loop, Revenue | Claude, n8n, Slack, Jev, Higgsfield, Twilio, Brevo, Metricool, Looker Studio, Postgres, HubSpot |
| 02 | Roofing office | about 23 (19 plus 4 brain) | Storm & leads, Front desk, Estimating, Claims, Scheduling, Follow-up & reviews | Claude, n8n, WhatsApp, Google Workspace, Google Business Profile, voice/phone tool |
| 01 | One-person social team | about 34 plus brain | Research, Content studio, Posting & community, Growth | Claude Code, n8n, Metricool, ManyChat, DeepL, ElevenLabs, Canva, Kit, Mollie, Calendly, Notion |

## Recurring design patterns
1. **Hub-and-spoke "brain" orchestrator.** A single coordinator routes, prioritizes and checks the work, and the departments hang off it. It goes by Research/Finance/Ads Brain, Claude CMO, Command Center, Head of Commerce, or "Claude Code runs it". Claude writes and decides, and n8n or Jev moves the work.
2. **One-page brief on a fixed cadence.** Daily morning page or Monday/Friday page with three parts: what happened, what is at risk, what to do next. Delivered via Slack, Gmail or Telegram, and often backed by Looker Studio.
3. **Single approval queue.** Nothing public, and no spend change beyond limits, without a human yes. Approvals happen in Slack, Telegram or WhatsApp. "The final yes is still yours."
4. **Three-tier agent permissions** (roofing map): Auto, Ask first, Never. These are written into `/rules/agent-permissions.md`, `approval-limits.md` and `banned-claims.md`.
5. **Shared knowledge files every agent reads.** Markdown folders for voice (with banned words), offer and pricing, audience, hooks, platform rules, community reply rules, reporting/KPI model. The point is that prompts never start from zero.
6. **"What interrupts the loop" event handlers.** Explicit triggers such as hail at 3 AM, a missed call, a quote silent for 2 days, a post that flops in hour one, a "how much?" DM, "stop emailing me", a meeting no-show, a discount request, or an agent breaking.
7. **Speed-to-lead under 60 seconds.** A voice agent (ElevenLabs plus Twilio) calls back form-fillers in their language and books on the call. Missed calls all route to one always-on number.
8. **Fixed follow-up cadence**: day 2, 5 and 10, at most 3 nudges, adapting to objections. Review link to every customer.
9. **Leads, not likes.** Attribution from post or ad to DM, lead, call and Stripe sale, which feeds the next week's plan (learning loop and winning-hook library).
10. **Generate many variants, keep the winners.** Ten variants per ad, hook libraries and hook scores, with automatic budget shifts within owner-set caps.
11. **Localization as a module.** Claude writes and DeepL translates or checks, for DE/FR/NL/ES. ElevenLabs dubs in the owner's voice.
12. **Consent-gated messaging.** A consent check (Usercentrics) before cart reminders, opted-in-only past-customer lists, AI self-disclosure in support, and a "GDPR Guard" agent.
13. **Observability layer.** LangSmith/Langfuse per-agent cost and error tracing, an agent activity log, and a Watchdog agent.
14. **Good/better/best quotes** and "send the quote to the phone first".

## Third-party tools
| Tool | Role in blueprints |
|---|---|
| Claude / Claude Code | Reasoning, writing, decisions; Claude Code as builder/orchestrator |
| Jev | Fast scoring/ranking/flagging and budget moves. **Never defined on any page.** Pink hexagon logo; possibly ReStructure's own engine or an unnamed vendor |
| n8n | Workflow automation and routing between agents |
| Higgsfield | AI video and graphics from scripts or product photos |
| ElevenLabs (incl. Agents) | Voiceover, dubbing, voice cloning, real-time voice call agents |
| Twilio | Telephony for voice agents |
| CapCut, Descript | Video editing; voiceover sync |
| Canva, Figma | Resizing per platform, carousels, brand kit, templates |
| DeepL | Translation and translation check |
| Apify | Scraping competitor or viral content and reviews |
| Google Trends, SparkToro, Semrush, Ahrefs, Reddit, TikTok Creative Center | Demand, audience and keyword research; trend and hook discovery |
| Trustpilot, Google Maps / Business Profile | Review mining, local competitor data, review requests |
| Dealfront | B2B website-visitor identification (intent) |
| Meta Ads, Google Ads, TikTok Ads | Ad platforms |
| CallRail | Call tracking for cost-per-lead |
| Google Tag Manager, Google Analytics, Unbounce | Tracking and landing pages (ad-agency/system maps) |
| HubSpot, Pipedrive | CRM |
| Cal.com, Calendly | Booking |
| Metricool, Buffer | Social scheduling and analytics |
| ManyChat | Instagram/Facebook comment and DM automation, lead tagging |
| Beehiiv, Kit, Brevo, Klaviyo | Email/newsletter, nurture, cart recovery |
| WhatsApp Business | Customer messaging, reminders, approvals |
| Slack, Telegram | Owner approvals and daily page delivery |
| Gmail | Contract intake, reports, insurer and collab mail |
| QuickBooks | Invoicing/ledger |
| Stripe, Mollie | Payments, payment links, sales attribution |
| Wise | Banking/cash view |
| Dext, Bill.com | Receipt capture, bills/AP |
| E-sign tool ("D" logo) | Contract signing (unconfirmed which) |
| Shopify | Store, orders, abandoned checkouts |
| Usercentrics | Consent management (CMP) lookups |
| Gorgias | Helpdesk inbox with human handoff |
| AfterShip | Order tracking |
| Loop Returns | Returns and exchange-first flow |
| Triple Whale | DTC profit and attribution |
| Asana | Project setup and tasks |
| Notion, Google Drive/Docs/Sheets, Airtable | Knowledge base, plans, hook libraries, budgets, test boards |
| Supermetrics, BigQuery, Looker Studio, PostgreSQL | Data pull, warehouse, dashboards, marketing DB |
| LangSmith, Langfuse | LLM/agent observability (cost, errors, traces) |
| Perplexity, OpenAI | Seen as logos only (research; thumbnail images) |

## Compliance issues noticed
- **AI outbound voice calls** (sales, agent-company, system, roofing front desk):
  - EU: ePrivacy and national unsolicited-call rules. Germany's UWG Section 7 requires prior express consent for B2C calls. Calling back someone who just submitted a form is usually covered, but the form must say so.
  - EU AI Act Article 50 (transparency obligations applying from Aug 2026) requires telling people they are talking to an AI.
  - US: TCPA. The FCC 2024 ruling treats AI-generated voices as "artificial/prerecorded voice", so prior express consent is needed.
  - Canada: CRTC rules and CASL for any electronic follow-ups.
  - Call recording consent (e.g. Germany Section 201 StGB).
  - The pages show a "GDPR Guard" box but no logic.
- **WhatsApp marketing** (store cart recovery, finance chaser, roofing): needs WhatsApp Business Platform templates, explicit WhatsApp-specific opt-in, and Meta's 24-hour session rules. The store page does say "opted-in only" and uses Usercentrics, which is the best practice shown in the set.
- **Email follow-ups and cart reminders**: GDPR and ePrivacy apply. Soft opt-in exists only for existing customers in some states. Canada's CASL needs express or implied consent plus identification and unsubscribe. US CAN-SPAM. The sales map handles "stop emailing me" as an event, but suppression lists are not designed.
- **Website visitor de-anonymisation** (Dealfront) and **scraping** (Apify on reviews, competitors, Reddit): GDPR lawful-basis and transparency duties, platform terms of service, database rights.
- **LinkedIn automated sending** (sales map): against LinkedIn's terms of service.
- **Voice cloning and dubbing in the owner's voice** and AI-generated ads (Higgsfield/ElevenLabs): AI Act deepfake labelling, platform AI-content labels, and consumer-protection rules on misleading ads (UCPD).
- **AI support and DM replies**: the store page discloses AI. The social and marketing pages do not mention disclosure.
- **Finance**: EU e-invoicing mandates and VAT rules are not mentioned. Automated dunning must respect the Late Payment Directive and must not threaten.
- **"Data stays in the EU" claim** (social-team): conflicts with the use of many US-hosted SaaS tools. DPAs, SCCs and region choices would be needed.
- **Earnings claims** (EUR 20K/month, EUR 100K/month, EUR 10,000+ value, -EUR 24K/year): unsubstantiated. Only the "system" page carries a disclaimer that the figures are illustrative.
