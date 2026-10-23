---
name: microsoft-ads-traffic
description: "Report Bing and Microsoft Advertising traffic and key events in Google Analytics (GA4) by source, medium and campaign, find paid clicks that arrive without UTM tags, and fix UTM and auto-tagging gaps. Use when the user asks how Bing Ads or Microsoft Ads traffic shows in Google Analytics, bing / cpc, bing / organic, UTM tags, msclkid, auto-tagging, campaign names in GA4, or why Analytics and Microsoft Advertising show different numbers."
---

# Bing and Microsoft Ads traffic in Google Analytics

The customer wants to know what their Microsoft Advertising clicks do on the
site, as Google Analytics (GA4) counts it, and whether those clicks are labelled
well enough to tell paid Bing visits from organic ones. You read Analytics
through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`. You cannot
read their Microsoft Advertising account, so this is what Analytics saw, never
what Microsoft Advertising billed or counted.

**Say this first, once.** Your first answer in this conversation opens with the
sentence below, in these words, and it is not repeated in later answers:

> Today: UET tag checks and staged tags in Tag Manager, Bing traffic and key events in GA4, UTM and auto-tagging hygiene, conversion goal guidance, Google Ads import prep (from the Google Ads account), responsive search ad drafts and budget math. Later: reading the Microsoft Advertising account when Microsoft approves AdCopilot's API access, with no date, as a plugin update adding a Microsoft connector key beside adcopilot.

Call `get_org_context` with `source: "claude-plugin/adcopilot-microsoft-ads/0.1.0"`
first, before any other tool, unless you already called it in this
conversation. Send `source` exactly as written, the version included. If this run
is a scheduled task with nobody there to answer, send `source: "claude-scheduled"`
instead and change nothing. `get_org_context`'s `next_step` and `playbook`
describe the whole workspace, not this request: do THIS request, keep any limit
`next_step` adds, and offer the rest afterwards.

If Google Analytics 4 is not connected, say what connecting it unlocks, in the
`unlocks` words `get_org_context` gives for it, and give the connect link
exactly as `get_org_context` returns it, never one from memory. Then stop:
invent no traffic number for a property you cannot read.

## The reads

`ga4_list_account_summaries` finds the properties. If there is more than one,
ask which, by the name Analytics shows. `ga4_get_metadata` lists the dimension
and metric names that property accepts, so use it rather than guess a name that
may be absent. `ga4_run_report` reads the numbers, and `ga4_list_conversion_events`
lists what the property counts as a key event (the tool keeps the older word,
conversion). Dates go in as `YYYY-MM-DD`, and you state the two ranges you
compare, by date, in the answer.

## What to answer

1. **Bing traffic as Analytics sorts it.** One report over the last 28 days and
   the 28 before: sessions, key events and revenue (when the property has any)
   by source and medium, narrowed to sources that contain `bing`. At the time of
   writing the names are `sessionSourceMedium`, `sessions`, `keyEvents` and
   `totalRevenue`; confirm them with `ga4_get_metadata` if the report refuses
   one. Show `bing / cpc` (paid) and `bing / organic` (unpaid search) as two
   different rows, each with its own numbers, and never add them together as
   "Bing". Then the same by campaign (`sessionCampaignName`) for the paid row.
2. **Paid clicks that arrive without UTM tags.** When a click reaches the site
   with no UTM tags, Analytics can only sort it by what it can see, such as the
   referrer, so a paid Bing visit can sit under `bing / organic` or under another
   source. The test is a report of sessions by `landingPagePlusQueryString`
   narrowed to addresses that contain `msclkid` (Microsoft's click ID, added by
   its auto-tagging), with `sessionSourceMedium` beside it. Sessions that carry
   `msclkid` but are not `bing / cpc` are paid clicks Analytics mislabelled:
   count them and show the top rows. If the report returns nothing, say that it
   cannot tell which of three things is true: auto-tagging is off, the
   property hides query strings from reports, or there were no paid clicks.
3. **Names that will not group.** From the paid row's campaign names, point out
   what splits one thing into several: `(not set)`, a campaign ID where a name
   is wanted, `Bing` against `bing`, `cpc` against `ppc` as the medium. Quote
   the values the report returned, and nothing you did not read.
4. **Key events.** From `ga4_list_conversion_events`, say whether the events the
   customer cares about are marked as key events, and give the `bing / cpc` count
   of each from the report. Analytics' key events and Microsoft Advertising's
   conversions are counted by different rules and will not match exactly: say
   so, and never call either one wrong because it differs.
5. **The fix, if there is a gap.** There are two ways to label paid clicks, and
   the customer picks one. They are changes in Microsoft Advertising, which you
   cannot make, so you write the exact text and they apply it.
   - **Microsoft's UTM tagging.** An account setting. Its API values are
     Inactive (adds nothing), Preserve (adds Microsoft's supported UTM tags and
     keeps any UTM tags already in the final URL) and Replace (adds them and
     overwrites the supported ones already there). The exact tags it adds are
     in Microsoft's help article "How do I add UTM tags to my landing page
     URL?"; read that before promising a campaign name or a keyword in them.
   - **Their own template.** A final URL suffix, or a tracking template that
     begins with `{lpurl}`, at account, campaign or ad group level (the lower
     level wins). The tracking-template example on Microsoft's own page uses
     `{Keyword}`, `{CampaignID}`, `{AdGroupID}` and `{AdID}`, and its
     final-URL-suffix example uses `{keyword}`: use those spellings and no other
     placeholder unless Microsoft's page "What tracking or URL parameters can I
     use?" lists it, and never invent one. A suffix may not start with `?`, `&`
     or `#`, and joins pairs with `&`. A readable campaign name comes from a
     custom parameter that they set on each campaign, written `{_campaign}` in
     the template; Microsoft takes up to 8 custom parameters per campaign, ad
     group or ad. A suffix that fits:
     `utm_source=bing&utm_medium=cpc&utm_campaign={_campaign}`.
     A template is limited to 2,048 characters.
   Use one method, not both, unless they have chosen Preserve on purpose. Give
   them one thing to check afterwards: click one of their own ads and read the
   address the landing page shows.
6. **Close with one next step**: the fix, a re-read of the same report in a few
   days once new clicks have arrived, or the `microsoft-ads-tracking` skill if
   conversions are missing from both sides.

## What this cannot see

Microsoft Advertising's own figures (spend, clicks, impressions, conversions),
their settings (auto-tagging and UTM tagging), and ad clicks that never reached
the site. A property that redacts query strings hides `msclkid` from these
reports. Say which of these limits matters to the answer you give.

## Changes

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill makes none itself: the labelling fixes above are made by the customer in Microsoft Advertising. Nothing is ever deleted. The numbers you give are the tool's numbers, never an invented one.

## Facts checked on 23 October 2026

From Microsoft's developer documentation on learn.microsoft.com: `msclkid` is a
32-character click ID that auto-tagging appends to the landing page address;
the UTM tagging values Inactive, Preserve and Replace; the tracking-template
rules and examples (`{lpurl}` required at account, campaign and ad group level,
2,048 characters, the placeholders above, custom parameters in the form
`{_name}`, at most 8); the final URL suffix rules. Microsoft Advertising's own
help pages could not be opened by a tool on that day, so for the exact tags its
UTM option adds and for any other placeholder, Microsoft's help page is the
referee.
