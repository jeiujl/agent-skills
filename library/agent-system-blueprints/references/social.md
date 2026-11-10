# Blueprint No. 01: One-person social media team

Source: https://restructure-europe.vercel.app/en/newsletter/social/ (loaded OK). The text gives 5 "steal this" tips. The full structure comes from the map image (`social-map.jpg`, high resolution). (logo) means the tool was identified from an icon.

## Purpose and audience
Solo creators and small brands. Research, content production, posting, community and growth run by agents, with one human approval queue.

## Structure (map)
- **Signals**: trending sounds (TikTok); search spikes (Google Trends); scraping competitors' posts (Apify); growth stats (Metricool); top videos by topic; most viewed (YouTube); real questions (Reddit); comment mining (Claude); DMs and keywords (ManyChat); collab requests (Gmail); link-in-bio clicks; site visits (Google Analytics).
- **System of record**: content calendar (Notion); raw footage (Google Drive); lead list; email list (Kit, formerly ConvertKit, logo); payments (Mollie, logo); booked calls (Calendly, logo); brand kit (Canva); templates (Figma).
- **Owner input**: voice and offer (Notion to Google Docs); goals (Sheets to Notion); raw material; approvals (WhatsApp/Telegram).
- **Brain, Claude Code**: triage, routes tasks (n8n), sets priorities (Notion), checks the work (Sheets).
- **What interrupts the loop**: trend spikes in your niche; competitor post blows up; someone asks "how much?"; post flops in the first hour; link clicks spike; negative comment blows up (goes to you); brand deal lands in inbox (goes to you); DM at 11pm (goes to you).

## Departments and agents (map: 34 department agents plus the brain)
| Department | Agents |
|---|---|
| Research (8) | Trend scout, Competitor watch, Hook analyst, Question miner, Keyword finder (Semrush to Ahrefs), Audience profiler, Idea bank, Content planner |
| Content studio (11) | Hook writer, Scriptwriter, Caption writer, Carousel designer (Canva/Figma), Thumbnail maker (Canva/OpenAI logo), Clip cutter, Video editor, Voiceover (ElevenLabs logo), B-roll finder, Brand checker, Translator (DeepL) |
| Posting & community (8) | Approval queue (Notion to WhatsApp), Scheduler (Metricool), Cross-poster, Comment replier, DM responder (ManyChat), Lead tagger, Email capture (Kit and ManyChat), Collab manager (Gmail to Notion) |
| Growth (7) | Analytics tracker, Link tracker, Revenue tracker (Mollie), Hook scorer, A/B tester, Ads manager (Meta/TikTok), Daily brief (Gmail) |

Triggers and outputs (from the text):
- Signals feed ideas. "The question you get most is your next post."
- The owner records one long take a week, and the studio cuts hooks, clips and captions from it.
- DeepL makes NL/DE/FR versions.
- Everything waits in one approval queue. After a yes, Metricool posts everywhere.
- A "how much?" comment makes ManyChat tag the lead and send a booking link.
- A post that flops in the first hour gets its hook rewritten.

## Knowledge layer (markdown files every agent reads)
- `/voice`: voice-guide, **banned-words**, tone-rules
- `/offer`: offer, pricing, faq
- `/content`: content-pillars, post-templates, video-scripts
- `/platforms`: tiktok-rules, instagram-rules, youtube-rules
- `/audience`: audience-profile, top-questions, pain-points
- `/hooks`: hook-library, hook-breakdowns, winning-patterns
- `/community`: reply-rules, dm-scripts, lead-tags
- `/reporting`: kpi-model, attribution-rules, daily-brief-template

## Human approval gates
- **Nothing posts without a human yes**, via a single queue.
- Negative-comment blow-ups, brand deals and late-night DMs escalate to the owner.

## Reports and KPIs
- One summary every morning (daily brief).
- Data panels: views and retention, followers, clicks and leads, revenue, agent activity log (Metricool, Looker Studio, Sheets).
- Core rule: **count leads/DMs, not likes or views**.

## Tools
Claude, Claude Code, n8n, TikTok, Google Trends, Apify, Metricool, YouTube, Reddit, ManyChat, Gmail, Google Analytics, Notion, Google Drive, Google Docs, Google Sheets, Kit, Mollie, Calendly, Canva, Figma, DeepL, ElevenLabs, Semrush, Ahrefs, OpenAI (logo), a clip tool (Opus Clip-like logo, unconfirmed), Meta, Instagram, WhatsApp, Telegram, Looker Studio.

## Claims (theirs)
None numeric. "The final yes is still yours."

## Gaps for a builder
- The contents of the files are not given. Only the file names are.
- The rewrite-hook-after-a-flop logic: whether it re-posts or edits, and how "flop" is measured.
- How the approval queue works on mobile.
- Consent for email capture from DMs (GDPR).
- ManyChat follows Meta's 24-hour messaging-window rules, which the page does not mention.
