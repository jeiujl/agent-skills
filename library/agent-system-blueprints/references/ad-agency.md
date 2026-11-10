# Blueprint No. 09: AI ad agency

Source: https://restructure-europe.vercel.app/en/newsletter/ad-agency/ (loaded OK, includes "How it's built" detail). (logo) means the tool was identified from an icon on the map.

## Purpose and audience
Replaces an outsourced paid-media agency for SMBs running Meta, TikTok and Google ads: planning, creative production, live optimization and learning.

## Departments / modules (claimed 35 agents across 4 layers)
**1. Campaign Strategist.** Trigger: the owner submits business, offer and budget.
- Platform Picker: Google Trends shows where demand is rising.
- Audience Builder: sets targeting in Meta Ads Manager and Google Ads.
- Budget Splitter: writes the budget allocation to Google Sheets.
- Test Planner: puts the first tests on an Airtable board.
- Output: a plan saying which platform, which audience, how to split the money and what to test first.

**2. Creative Studio.** Trigger: the strategy arrives from the Strategist.
- Hook Writer and Script Writer (Claude): write hooks, headlines and video scripts.
- Video Ad Maker: Higgsfield plus CapCut.
- Voiceover: ElevenLabs, synced in Descript.
- Variation Builder: makes **10 versions per ad**.
- Output: ad variants. **Only the ones the owner approves launch.**

**3. Performance Monitor.** Trigger: an ad goes live; runs 24/7.
- Spend Watcher: Meta Ads Manager and TikTok Ads Manager.
- Lead Cost Tracker: HubSpot leads and CallRail calls.
- Return Tracker: Stripe sales.
- Budget Mover: uses Jev to shift spend from dying ads to sellers, "within your limits".

**4. Ads Brain.** Trigger: every result from the Monitor.
- Router: Claude assigns work and n8n moves it.
- Learning Loop: Claude works out what worked, updates the winning-hooks library in Notion and feeds the Strategist.
- Approval Gate: Claude checks every ad.
- Spend Guard: keeps Jev inside spend limits.

**5. Monday page.** One page: spend, return, and where to add money next week.

## Tools
Claude, Jev, n8n, Google Trends, Meta Ads Manager, Google Ads, TikTok Ads Manager, Google Sheets, Airtable, Higgsfield, CapCut, ElevenLabs, Descript, HubSpot, CallRail, Stripe, Notion. From map logos: Gmail, Looker Studio, Slack, Google Tag Manager, Unbounce, plus two unidentified (a blue arrow icon and a black bar icon).

## Human approval gates
- The owner approves which creative variants launch.
- Claude runs an automated approval check on every ad (a policy/brand check).
- Budget moves are automatic but bounded by owner-set limits (Spend Guard). No numbers are given.

## Data / memory
- Notion "winning hooks" library, updated by the Learning Loop.
- Sheets holds the budget plan and Airtable the test board.

## Reports and KPIs
- Monday one-pager.
- KPIs: spend, cost per lead (HubSpot plus CallRail), return on ad spend (Stripe), ad decay ("starts dying").

## Claims (theirs)
- "Replace your entire ad agency".
- 35 agents.
- 24/7 optimization.
- 10 variants before an agency would send a first draft.
- "Makes you money every single day".

## Gaps for a builder
- No definition of "dying": which metric, what window, how many conversions before acting. The statistical-significance rules are missing.
- No numeric spend limits or caps on daily reallocation, and no rollback.
- No attribution model linking Stripe sales to ads (UTMs, CAPI, offline conversions).
- Ad-platform policy review and the EU DSA/political-ad rules are not addressed.
- AI-generated likeness/voice rights and disclosure for Higgsfield/ElevenLabs ads are not covered.
- API access requirements (Meta Marketing API app review, TikTok and Google developer tokens) are not mentioned.
