# Blueprint No. 06: AI social media team (multi-country)

Source: https://restructure-europe.vercel.app/en/newsletter/social-team/ (loaded OK, includes "How it's built" detail). The map shows these stages: plans, creates, every country, best time, posts, learns, replies, converts.

## Purpose and audience
EU brands selling across several countries. One idea becomes localized content per market, and comments and DMs are converted into sales.

## Modules (agent count not stated on the page)
**1. Content Studio.** Trigger: weekly planning.
- Hook Finder: Apify pulls videos that are working in the market, plus a hook library in Airtable.
- Script Writer (Claude): a full week of scripts per market.
- Video Maker (Higgsfield): turns product photos into videos.
- Voice & Dubbing (ElevenLabs): FR, DE and ES in the owner's own cloned voice.
- Everything waits at the Approval Desk.

**2. Publishing.** Trigger: the owner approves in Slack.
- Formatter: Claude writes per-language captions, and Canva resizes per platform.
- Jev picks the best time per country and platform.
- Scheduler (Buffer) queues posts.
- Short-Form and Long-Form Posters publish to TikTok, Instagram, YouTube Studio and LinkedIn (the map also shows Facebook).
- After publishing, results are reviewed and more of what worked is made.

**3. Comments to customers.** Trigger: any comment or DM.
- Comment Watcher: ManyChat and Facebook.
- Reply Agent: Claude replies in the customer's language, checked by DeepL.
- Buyer Spotter: Jev identifies buyers and saves them to HubSpot.
- Link Sender: sends a Stripe payment link.
- Call Booker: books via Calendly.
- Ready buyers are routed to the human team.
- The map example shows replies labelled "AI assistant".

**4. Morning page.** Trigger: daily.
- Claude Code runs the team, and Jev and n8n route tasks.
- The Morning Reporter builds a Looker Studio view: Metricool views by country, ManyChat reply time, HubSpot/Calendly leads and calls, Stripe sales by country. It sends one page to Slack.
- LangSmith traces agents.

## Tools
Claude, Claude Code, Jev, n8n, Apify, Airtable, Higgsfield, ElevenLabs, Slack, Canva, Buffer, TikTok, Instagram, YouTube Studio, LinkedIn, Facebook, ManyChat, DeepL, HubSpot, Stripe (payment links), Calendly, Metricool, Looker Studio, LangSmith.

## Human approval gates
- All content is approved in Slack before formatting and scheduling.
- Hot buyers are handed to the human team.
- Comment replies, payment links and bookings appear autonomous.

## Data / memory
- Airtable hook library.
- The page claims customer data is kept in the EU.

## Reports and KPIs
- Daily page: posts that worked, DMs that became sales, what to post next.
- KPIs: views by country, reply time, leads, calls, sales by country.

## Claims (theirs)
- The map headline shows "Social media agency per year: -EUR 24,000" (implied saving).
- "Without hiring a team in each country."
- "Built to keep customer data in the EU". Many of the listed tools are US-hosted, so this claim needs verification.

## Gaps for a builder
- The **voice-cloning** consent and contract for the owner's voice is not addressed.
- AI disclosure on dubbed or synthetic video (EU AI Act Article 50 transparency, platform AI labels) is not covered.
- EU data residency is asserted, but no regions or DPAs/SCCs are listed for Claude, HubSpot, ManyChat or Stripe.
- No rules for when the Reply Agent must not answer (complaints, legal, refunds) and no limits on its pricing claims.
- How "best time" is computed, and no agent count.
- Apify scraping of competitor content raises copyright and terms-of-service questions.
