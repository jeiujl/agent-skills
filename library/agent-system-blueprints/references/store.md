# Blueprint No. 05: AI system for Shopify stores

Source: https://restructure-europe.vercel.app/en/newsletter/store/ (loaded OK, includes "How it's built" detail). The map shows 8 departments: Ad Studio, 3 Languages, Paid Ads, Repeat Buyers, Cart Recovery, Support, Profit Guard and Morning Page.

## Purpose and audience
Shopify DTC stores selling into several EU countries (DE/FR/NL). Covers ads, cart recovery, support, repeat purchase and profit.

## Modules (claimed 8 departments, 41 agents)
**1. Ad Creative Studio.** Trigger: ongoing hook research.
- Hook Finder: Apify plus TikTok Creative Center.
- Hook Picker: Jev keeps the hooks that sell (the map shows hook scores such as 94, 91 and 88).
- Script Writer: Claude plus DeepL, in DE, FR and NL.
- Video Maker: Higgsfield turns product photos into video, and ElevenLabs adds the voiceover.
- Owner signs off at the Approval Desk.

**2. Cart recovery.** Trigger: an abandoned checkout in Shopify; n8n fires **within the hour**.
- Consent Checker: queries Usercentrics.
- Reminder Writer: Claude plus DeepL, giving "a real reason to come back".
- Reminder Sender: Klaviyo or WhatsApp Business, **to opted-in customers only**.
- Discount Guard: Jev decides who actually needs a discount.

**3. Customer support.** Trigger: an inbound email, chat or DM.
- Support Inbox: Gorgias, with Shopify order context.
- Answer Agent: Claude, **discloses that it is AI**, uses DeepL for the customer's language.
- Order Tracker: AfterShip.
- Returns Agent: Loop Returns, offering an exchange first.
- A request for a human is handed off via Gorgias.

**4. Head of Commerce (Claude Code).**
- Claude Code orchestrates, and Jev and n8n route work. Claude checks consent and AI disclosure.
- Profit Tracker: per-order profit in Triple Whale.
- Morning Reporter: Looker Studio, plus a one-page summary in Slack.

The map also shows these modules, which the text does not describe:
- **Paid Ads**: per-country budget bars, one shown as "paused", with a Creative Analyst.
- **Repeat Buyers**: Next-Order Finder and Repeat Planner, Klaviyo icon.
- **Profit Guard**: Discount Guard, "no new spend".

## Tools
Claude, Claude Code, Jev, n8n, Apify, TikTok Creative Center, DeepL, Higgsfield, ElevenLabs, Shopify, Usercentrics, Klaviyo, WhatsApp Business, Gorgias, AfterShip, Loop Returns, Triple Whale, Looker Studio, Slack, Telegram.

## Human approval gates
- Ads are approved at the Approval Desk (Slack or Telegram).
- **Discounts are approved by the owner** in Slack or Telegram.
- Support hands off to a human on request.
- The map's morning page shows "2 ads waiting for you: APPROVE".

## Data / memory
- Shopify order history, Usercentrics consent records, and the Triple Whale profit model.

## Reports and KPIs
- Daily one page of "what made you money". The map example shows a winning ad at +EUR 1,420 (DE) and cart reminders at +EUR 860 from 18 orders.
- KPIs: profit per order, recovered revenue, ad winners by country.

## Claims (theirs)
- 41 agents.
- About 7 of 10 carts are abandoned.
- "That's how you get to EUR 100,000 a month."
- "No need to hire another support person."

## Gaps for a builder
- WhatsApp marketing requires an approved WhatsApp Business API template and opt-in specifically for WhatsApp. The page names WhatsApp Business without saying whether that means the API or the app.
- Discount rules: margin floors and frequency caps are not given.
- Policy boundaries for the support agent: refunds, chargebacks and legal threats.
- How the EU AI Act disclosure is worded, and how consumer-law withdrawal rights (14-day returns) are handled in the returns flow.
- Paid Ads, Repeat Buyers and Profit Guard are undocumented in the text.
- No breakdown of the 41 agents.
