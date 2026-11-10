---
name: agent-system-blueprints
description: "Design a done-for-you AI agent system for a client business (sales, marketing, social, ads, finance, market research, e-commerce, trades front office or a whole-company 'brain'), using 11 worked blueprints and the patterns they share: one coordinator, shared knowledge files, auto / ask-first / never permissions, one approval queue, event triggers, speed-to-lead, a one-page brief, and lead-to-sale tracking. Use when scoping, pitching, pricing or building an agentic system for a client, or turning a discovery call into a system map."
---

# Agent system blueprints

Use this to turn "we want AI to run our X" into a concrete system map a client can approve and you can build. The references are summaries of 11 public blueprints from ReStructure AI Europe (Nov 2026), written in our own words. Their agent counts and revenue figures are their marketing claims: never repeat them to a client as facts.

## Pick the starting blueprint
Read `references/overview.md` first (summary table, shared patterns, tool list, compliance notes). Then open only the one or two blueprints that match:

| Client need | Blueprint file |
|---|---|
| Find, call back and follow up leads; book meetings | `sales.md` |
| Run marketing with one person (content, email, analytics) | `marketing-team.md`, `system.md` |
| Social media: posts, video, comments into customers | `social.md`, `social-team.md` |
| Paid ads on Meta, Google, TikTok | `ad-agency.md` (pair with the `ai-ads-strategist` / `claude-ads-ads` skills) |
| Invoices, payment chasing, cash view | `financial-os.md` |
| Competitors, customer voice, demand, pricing | `market-research.md` |
| Shopify / e-commerce | `store.md` |
| Trades or field-service office (calls, quotes, scheduling, reviews) | `roof.md` |
| Whole company with one shared brain | `agent-company.md` |

## Design the system (in this order)
1. **Outcome and owner.** One sentence: what the system produces (booked calls, paid invoices, posts that bring DMs) and which person owns the yes.
2. **Modules.** 3–6 modules, not 35 agents. For each agent: job, trigger, inputs, output, tool. Merge anything a single prompt can do. Clients buy outcomes, not agent counts.
3. **The coordinator.** One hub that routes work, checks it and writes the brief (Claude / Claude Code, with n8n or similar moving data). Say where it runs and who can see the data.
4. **Shared knowledge files** every agent reads, so prompts never start from zero: `voice.md` (with banned words), `offer-and-pricing.md`, `audience.md`, `faq-and-reply-rules.md`, `platform-rules.md`, `kpis.md`. These are also the first deliverable, and the "Business Brain" offer.
5. **Permissions in three tiers**, written down in `agent-permissions.md` and `approval-limits.md`:
   - **Auto:** internal drafts, tagging, reminders to the owner, reports.
   - **Ask first:** anything a customer sees, any spend or budget move, quotes over a set amount, refunds.
   - **Never:** claims in `banned-claims.md`, messaging people without consent, deleting data, changing prices.
6. **One approval queue** in the tool the owner already uses (Slack, WhatsApp, email). The final yes stays with a person.
7. **Event triggers.** List what interrupts the loop: missed call, form fill, "how much?" message, quote silent 2 days, no-show, "stop emailing me", post flops in hour one, payment 7 days late, an agent failing. Each gets a defined response.
8. **Speed and follow-up rules.** Reply to new leads in under 5 minutes, under 60 seconds where possible. Follow up on day 2, 5 and 10, at most 3 nudges, then stop. Ask every paying customer for a review.
9. **One-page brief** on a fixed schedule (daily or Monday): what happened, what's at risk, the top 3 decisions needed.
10. **Track leads, not likes.** Connect post or ad → lead → call → sale (CRM + payments), and feed the winners back into next week's plan.
11. **Observability.** Log each agent's actions, cost and errors (an activity log at minimum; LangSmith or Langfuse for bigger builds) and alert a person when something breaks.

## Compliance check before building (Canada first)
- **CASL** for any email, text or DM from Canada: express or implied consent, sender ID, unsubscribe. CAN-SPAM / TCPA for US recipients; GDPR and the EU AI Act for EU.
- **AI voice calls:** disclose it's an AI at the start, call back only people who asked (say so on the form), follow the CRTC and National DNCL rules, and get consent before recording.
- **WhatsApp and SMS marketing** need opt-in. A trade-show badge scan is not consent.
- **Voice cloning** only of the client's own voice, with written permission.
- **Scraping:** public business data only. No LinkedIn scraping or automated LinkedIn sending (against its terms).
- No invented results, reviews or revenue claims in anything the system publishes.

## Deliverable
Write a one-page **system map** for the client: outcome, modules (agents, triggers, tools), knowledge files, permission tiers, events, brief schedule, KPIs, compliance notes, and what the client must supply (account access, a named responder, approvals within 48 h). Then a build plan in phases (start with one module that pays back fastest, usually speed-to-lead) and the price, using the Onvlo/Flowa offers and the `pricing` skill.
