# Blueprint No. 02: AI roofing office

Source: https://restructure-europe.vercel.app/en/newsletter/roof/ (loaded OK). The page text gives 4 "steal this" tips. The full structure comes from the map image (`roof-map.jpg`, high resolution and legible). The setting is a German-speaking roofing contractor.

## Purpose and audience
Roofing contractors, especially storm/hail-driven ones: lead capture after storms, phone answering, fast quotes, insurance claims, crew scheduling and reviews.

## Structure (map)
- **Signals**: hail and storms; new enquiries (phone, then WhatsApp, then CRM); reviews (Google Business Profile); insurer mail (Gmail); ads (Google Ads, Meta); suppliers.
- **System of record**: customers and jobs (CRM, green hex icon, unidentified); buildings and roofs; calendar (Google Calendar); photos and files (Google Drive); price book (Google Sheets); money (accounting tool, red X icon, unidentified).
- **Owner input**: price book and margins (Sheets); service area and capacity (Maps); rules; approvals (WhatsApp).
- **Brain / Command center**: Chief of Staff agent (WhatsApp), Priority agent (Claude), Approval agent (WhatsApp), Watchdog agent (n8n).
- **What interrupts the loop**: hail at 3 AM; missed call on the roof; quote quiet for 2 days; rain on an open-roof day; appraiser asks for photos; bad review; late delivery; an agent breaks.

## Departments and agents (map: about 19 department agents plus 4 brain agents)
| Department | Agents | Trigger | Inputs | Outputs |
|---|---|---|---|---|
| Storm & leads | Storm scout, Lead agent, Ads agent, Route agent | Hail event | Hail size per roof, roof age, opted-in past-customer list | Prioritized roofs (hardest hit and older first); messages to **opted-in** past customers; ads |
| Front desk | Voice agent, Chat agent, Booking agent | Call or chat, 24/7, in German | Address, hail data | Inspection booked |
| Estimating | Measure agent, Pricing agent, Quote agent | Inspection done | 3D model and aerial imagery; price book | **Good/better/best** quote sent to the customer's phone (WhatsApp) |
| Claims | Evidence agent, File agent, Appraiser agent | Insurance job | Photos (Drive), insurer email | Damage file; appraiser coordination |
| Scheduling | Crew agent, Weather agent, Material agent | Job won | Calendar, weather, suppliers | Crew plans; rain-day moves; material orders |
| Follow-up & reviews | Nudge agent, Review agent, Referral agent | Quote silent from day 2; job done | Quote status | Up to **3 reminders max**; review link to **every** customer; referral asks |

**Data and observability**: revenue and pipeline, storm opportunity, response times, crew utilisation, agent activity log. **Human handoff**: you (approvals), roofer on site, the appraiser, your customers.

## Agent permissions (the most reusable artifact in the set)
- **Auto**: answer every call and chat; book inspections; score every roof after hail; measure roofs and draft quotes; message past customers who opted in; move crews off rain days.
- **Ask first**: discounts; sending a damage file to the insurer; ad spend above the weekly cap; overtime or extra scaffolding; public replies to reviews.
- **Never**: knock on doors; message anyone without consent; promise what the insurer will pay; change the price book; sign orders.

## Knowledge layer (markdown files)
- `/pricing`: price-book, waste-rules, financing
- `/materials`: tiles-and-hail-classes, underlays, suppliers
- `/storms`: hail-thresholds, storm-playbook, postcodes
- `/insurance`: appraiser-checklist, damage-file, insurers
- `/crews`: crews, capacity, safety-rules
- `/customers`: service-area, faq, past-customers
- `/brand`: tone-of-voice, photos, reviews
- `/rules`: agent-permissions, approval-limits, banned-claims

## Tools
Claude, n8n, WhatsApp, a phone/voice tool (black "S" icon, possibly sipgate; unconfirmed), Google Business Profile, Gmail, Google Ads, Meta, Google Calendar, Google Drive, Google Sheets, Google Maps, plus the unidentified CRM and accounting tools. Hail-data and 3D/aerial roof-measurement providers are implied but not named.

## Reports and KPIs
- Response times, crew utilisation, storm opportunity, revenue and pipeline, agent log.
- No daily page is described explicitly on this page.

## Claims (theirs)
- No revenue claims.
- "The first good quote on their phone usually wins".
- "The final yes is still yours."

## Gaps for a builder
- No hail-data source or roof-measurement vendor is named.
- The CRM and accounting tools are unclear.
- The "weekly cap" value for ad spend is not given.
- Voice-agent AI disclosure is not covered.
- Recording-consent rules in Germany (Section 201 StGB) are not covered.
- WhatsApp Business API opt-in is not covered.
