# Blueprint No. 03: Claude AI marketing system ("Claude CMO")

Source: https://restructure-europe.vercel.app/en/newsletter/system/ (loaded OK). The text is brief and generic. Tools come from the map image (`system-map.jpg`).

## Purpose and audience
SMB marketing. One orchestrator ("Claude CMO") coordinates six teams, from research to reporting.

## Structure (map: "6 teams live, 35 agents")
**Claude CMO (orchestrator)** has five controls: Router (n8n logo), Approvals (Slack), Budget (Jev), Compliance (shield icon) and Monday report (Gmail).

**Signals in**: Meta, Google Ads, a black form/voice icon, WhatsApp Business, a purple square icon and Google Business Profile. Several icons are unidentified.

| Team | Job | Trigger | Tools (logo) |
|---|---|---|---|
| Market Intel | Research; turns signals into context | Incoming signals | Search, Claude |
| Ad Factory | Make video ads | Briefs from the CMO | Higgsfield, ElevenLabs (logo) |
| Launch | Launch ads | Approved creative | Meta, Google Ads |
| Speed-to-Lead | Call new leads | New lead | Form tool, Twilio |
| Money Loop | Follow-ups | Unconverted leads | Brevo, Metricool (logo) |
| Revenue | Reporting | Weekly | Looker Studio, Google Analytics |

**Data layer**: Knowledge (Notion), Marketing DB (PostgreSQL), CRM (HubSpot), Timeline (unidentified green icon).

## Human approval gates
- An "Approvals" control in the orchestrator (Slack), plus Budget and Compliance controls.
- No thresholds or criteria are given.

## Data / memory
- Shared knowledge, marketing DB, CRM and timeline. The page stresses that teams share operational data instead of treating each message as a separate task.

## Reports and KPIs
- Monday report (email). No KPIs are listed.

## Claims (theirs)
- 35 agents and 6 teams.
- The page itself says the figures in the video are **illustrative and not a performance guarantee**. It is the most cautious page of the set.

## Gaps for a builder
Almost everything:
- No per-agent detail.
- No compliance rules behind the "Compliance" box.
- No budget limits.
- No lead-calling consent model.
- No schema for the "timeline".
This page is essentially a teaser for a sales call.
