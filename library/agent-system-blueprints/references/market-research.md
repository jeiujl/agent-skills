# Blueprint No. 11: AI market research system

Source: https://restructure-europe.vercel.app/en/newsletter/market-research/ (loaded OK). Page text is short; module names, agent counts and most tools come from the map image (`market-research-map.jpg`). Tools marked (logo) were identified from icons, not named in the text.

## Purpose and audience
A competitive and demand intelligence loop for **local businesses** in Europe. It tells the owner where competitors are weak, how customers describe what they want, and when demand is rising.

## Departments / modules (map: 7 modules x 5 agents = 35, plus Knowledge and You)
| Module | Agents (claimed count) | Trigger | Inputs | Outputs |
|---|---|---|---|---|
| Competitor Intel | 5 | Weekly schedule | Top local competitors' offers, prices and reviews. Google Maps and Apify (logo) | Gap list: services nobody offers, complaints nobody fixes. Claude writes it |
| Customer Voice (miner) | 5 | Not stated (assumed weekly) | Hundreds of reviews and comments in DE/FR/NL etc. Trustpilot and Reddit (logo) | Buyer phrasing: the exact words customers use when they are ready to buy, for use in copy |
| Demand Radar | 5 | Continuous/periodic | Local search interest. Google Trends (logo) | List of rising searches. Jev flags the fast risers |
| Translation | 5 | Whenever non-English sources arrive | Multilingual reviews and comments. DeepL and Perplexity (logo) | Normalized text in the operator's language |
| Price Tracker | 5 | Periodic | Competitor price points. Google Business Profile and Semrush (logo) | Price comparison (map shows example tags of EUR 49/65/80) |
| Social Listening | 5 | Periodic | Instagram and TikTok (logo) | Social mentions and trends |
| Research Brain | Orchestrator | Runs all modules | All module outputs | The Monday page |
| Knowledge | none | n/a | Notion and Google Drive (logo) | Shared context |
| You: Monday Page | none | Every Monday | Brain summary | Delivered by Gmail/Slack (logo) |

## Tools and integrations
Claude (reasoning and writing), Jev (scoring and flagging trends; the page never explains what Jev is), Google Maps, Apify (logo), Trustpilot (logo), Reddit (logo), Google Trends (logo), DeepL (logo), Perplexity (logo), Google Business Profile (logo), Semrush (logo), Instagram, TikTok, Notion, Google Drive, Gmail, Slack.

## Human approval gates
None stated. The output is advisory: the owner reads the page and decides what to launch.

## Data / memory
A "Knowledge" module (Notion and Drive) feeds the brain. The page does not say what files it holds.

## Reports and KPIs
- **Monday one-pager** covering market changes, what customers are asking for, and the single next offer to launch.
- No metrics are defined beyond that.

## Claims (theirs)
- "Worth over EUR 10,000 to any local business" (map headline: "EUR 10,000+").
- One wrong market decision can cost "tens of thousands of euros".
- 35 agents.

## Gaps for a builder
- No competitor-selection logic: how "top local competitors" are chosen, what radius, how many.
- Scraping legality and terms of service for Google Maps reviews, Trustpilot and Reddit are not covered. Neither is GDPR treatment of reviewer names and personal data.
- "Jev" is never defined: it may be a vendor or ReStructure's own scoring layer.
- No scoring rubric for gaps or for "the one offer to launch next".
- No storage schema, deduplication or history to show "what changed" week over week.
- No cost or volume figures (API calls, Apify credits).
- The roles of Translation and Social Listening, and what their 5 agents each do, are not described.
