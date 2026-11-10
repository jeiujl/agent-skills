# Blueprint No. 07: One-person marketing team

Source: https://restructure-europe.vercel.app/en/newsletter/marketing-team/ (loaded OK, includes "How it's built" detail). The map alt text lists the departments: research and content, creative studio, distribution and community, analytics loop, email and nurture, leads and booking, search and website. The brain is Claude Code.

## Purpose and audience
Solo founders and very small teams who want research, content, posting, email and analytics run by agents. The claim is "feels like 23 employees, 36 agents".

## Modules
**1. Research and content.** Trigger: continuous/weekly research.
- Trend Spotter, Audience Researcher and Keyword Finder read Google Trends, SparkToro, Reddit and Semrush.
- Post Writer and Email Writer (Claude) write posts, newsletters and sequences from the voice/offer docs in Notion.
- **No post goes live without approval.**

**2. Creative and distribution.** Trigger: drafts from the Post Writer.
- Video Maker: Higgsfield for graphics and short videos, ElevenLabs for voice.
- Approval Desk: sends finished posts to the owner in Slack.
- Scheduler: only approved posts. It picks the best hour in Metricool and posts to all channels.
- Comment & DM Agent: ManyChat plus Claude, replying in the owner's voice.

**3. Analytics loop.** Trigger: post performance data.
- Post Analyst: Metricool reach, saves and shares, with Claude explaining why a post worked.
- Jev attributes calls and sales to posts using Calendly/HubSpot bookings and Stripe sales by post.
- Loop Feeder: writes next week's plan in Notion.

**4. Morning page / brain.** Trigger: daily.
- Claude Code connects the CRM, calendar and channels. Jev and n8n route signals, and LangSmith traces agents.
- The page pulls Metricool posts and reach, HubSpot leads by post, Calendly calls, Beehiiv opens and clicks, and Stripe sales, all into Looker Studio.
- Approvals happen in Slack or Telegram.

The other map departments (Email and nurture, Leads and booking, Search and website) are not described in the text.

## Tools
Claude, Claude Code, Jev, n8n, LangSmith, Google Trends, SparkToro, Reddit, Semrush, Notion, Higgsfield, ElevenLabs, Slack, Telegram, Metricool, ManyChat, Calendly, HubSpot, Stripe, Beehiiv, Looker Studio.

## Human approval gates
- Every post is approved in Slack or Telegram before scheduling.
- Comment and DM replies appear automatic: no gate is mentioned.
- Tagline: "AI moves the information. You move the brand and the budget."

## Data / memory
- Notion holds the voice and offer docs that writers read, and the weekly plan written back by the Loop Feeder.

## Reports and KPIs
- **Daily morning page**: what worked, what is booked, what is next.
- KPIs: reach, saves, shares, leads by post, calls booked, email opens and clicks, sales by post. The emphasis is on revenue attribution over vanity metrics.

## Claims (theirs)
- 36 agents, equivalent to 23 employees.
- Always posting what people want "before your competitors do".

## Gaps for a builder
- Email and nurture, Leads and booking, and Search and website are unspecified.
- How post-to-sale attribution actually works: UTM/link scheme, Stripe metadata.
- Guardrails for auto-replies: escalation rules, banned topics, AI disclosure.
- Email consent and double opt-in for Beehiiv lists under GDPR.
- No posting volume, cost or agent breakdown.
