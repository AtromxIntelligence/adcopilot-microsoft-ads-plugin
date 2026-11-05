---
name: microsoft-ads-plan
description: "Plan Microsoft Ads (Bing Ads) from the customer's Google Ads account: which campaigns to bring over with Microsoft Advertising's Import from Google Ads, what to fix first, what budget to test, and responsive search ad drafts. Use when the user asks to start on Bing, import Google Ads campaigns into Microsoft Ads, write Bing ad copy or responsive search ads, or plan a Microsoft Advertising budget."
---

# Microsoft Ads plan and copy

The customer wants to start on Microsoft Ads (Bing Ads), or to improve it, and
has Google Ads to start from. The plan and the copy are your own work. The
only account AdCopilot reads for this is their Google Ads account, through the
connector at `https://mcp.adcopilot.cloud/mcp`, and everything you read there is
Google data and is labelled as Google data. AdCopilot reads no Microsoft
Advertising data for this, and you say so once, plainly.

**Say this first, once.** Your first answer in this conversation opens with the
sentence below, in these words, and it is not repeated in later answers:

> Today AdCopilot checks your Microsoft Advertising UET tag in Google Tag Manager and stages tags there for you to publish, reports Bing traffic and key events in Google Analytics (GA4), finds UTM and auto-tagging gaps, guides conversion goal setup, prepares a Google Ads import from your Google Ads account, drafts responsive search ad copy and does the budget pacing math. It cannot read your Microsoft Advertising account yet: that part of AdCopilot is being built, and there is no date yet.

Call `get_org_context` with `source: "claude-plugin/adcopilot-microsoft-ads/0.1.2"`
first, before any other tool, unless you already called it in this
conversation. Send `source` exactly as written, the version included. If this run
is a scheduled task with nobody there to answer, send `source: "claude-scheduled"`
instead and change nothing. `get_org_context`'s `next_step` and `playbook`
describe the whole workspace, not this request: do THIS request, keep any limit
`next_step` adds, and offer the rest afterwards.

If Google Ads is not connected, say what connecting it unlocks, in the `unlocks`
words `get_org_context` gives for it, and give the connect link exactly as
`get_org_context` returns it, never one from memory. Then stop reading. The
ad copy below does not need the connection: if they want copy, ask for the page
address, the offer and the audience, and write from what they say.

## Which Google account

`list_accessible_customers`, and the enabled accounts `get_org_context` reports,
say which Google Ads accounts there are. If more than one could be the source,
ask which, by the name Google Ads shows. A manager account has no campaigns of
its own, so it is never the source. Say which account you read, right after your
first sentence.

## The import plan

1. **Read what Google Ads holds.** One `search` of the campaigns over the last
   30 days: name, status, type, budget, cost and conversions. Use
   `get_resource_metadata` for the field names rather than guessing them.
   Google reports money in micros (millionths of the currency): divide by
   1,000,000 once, name the account's currency, and never print a micros number
   as money.
2. **Fix first, import second.** An import copies what is in the account,
   including what wastes money. Run `analyze_waste`, and say what the biggest
   waste is before they copy it. Run `conversion_setup_audit`, and say whether
   Google Ads counts results properly. An import does not put a Microsoft
   tracking tag on their site: results in Microsoft Advertising are counted by
   its UET tag, so the `microsoft-ads-tracking` skill comes before they judge
   any imported campaign by its conversions.
3. **Which campaigns first.** Suggest the one or two with conversions at a cost
   they accept, and say this is your judgement and not Microsoft's rule. Which
   campaign types Microsoft Advertising imports, and what an import leaves
   behind, are in its help article "What gets imported", which is the referee:
   never tell them a type will or will not come across.
4. **The import itself is theirs to run**, in Microsoft Advertising, under
   Import from Google Ads, then Choose import options (checked 23 October 2026
   in Microsoft's documentation). Tell them the options that move money, in
   plain words:
   - Bids and budgets can be raised or lowered by a percentage (Microsoft's
     range is -90 to 900), so a test can start smaller than Google Ads.
   - Increasing campaign budgets to Microsoft's minimum is on by default, and a
     budget below the minimum is raised: the spend can be higher than the Google
     Ads figure. If they turn it off, a campaign below the minimum is not
     imported.
   - Currency conversion is offered only when the two accounts use different
     currencies, and is off unless chosen: compare the first imported budgets
     with the Google Ads figures, each in its own account's currency.
   - The import can run now, once, or on a schedule (Auto, Daily, Weekly,
     Monthly). A recurring import keeps copying what changes in Google Ads;
     deleting what was removed in Google Ads is a separate option that is off
     by default. Ask which they want, and do not choose for them.
   - The Google sign-in Microsoft asks for is theirs: AdCopilot is not part of
     it and sees nothing of it.
5. **A first budget.** Ask what they can afford to test per month, in their
   currency. Put it beside the Google figure you read and show the arithmetic,
   with the currency named. The daily figure is the month's amount divided by
   the days in the month, and you say which month. Never say what Bing will
   return for it: AdCopilot has no Microsoft data to say so with.
6. **After the import, before anything goes live**, tell them to look in
   Microsoft Advertising at each imported campaign's status, budget and
   currency, and then to run the `microsoft-ads-tracking` skill and the
   `microsoft-ads-traffic` skill, so results are counted and labelled from the
   first click.

## Responsive search ad drafts

Microsoft's limits, checked 23 October 2026 in its API documentation: a
responsive search ad takes 3 to 15 headlines of up to 30 characters each and 2
to 4 descriptions of up to 90 characters each; each of the two display path
parts takes up to 15 characters, and the domain together with both may not
exceed 67; a final URL may be up to 2,048 characters. For languages with
double-width characters (Korean, Japanese, Chinese, and emoji) the limits are
about halved: 15 for a headline, 45 for a description, 7 for a path part and
33 for the domain with both paths. Text may carry dynamic
text such as `{keyword}`, which counts after substitution, so give it a default.
Unless a line is pinned to a position, Microsoft chooses the layout for each
search, so pin only what must stay in place and say that each pin reduces the
combinations.

Write from facts the customer gave you or that their page or their Google ads
already say, and label the Google ones. Never invent a price, an offer, an
award, a guarantee, a review count or a delivery time. Count every line
yourself and show the count in brackets beside it, for example `Plumbers In Leeds (17)`;
a line over its limit is not offered. Give a spread: the keyword's own words,
a benefit, proof they supplied, and a call to action, with no two lines the
same. Microsoft's editorial review is the referee on anything else; say so
rather than promising approval. The customer pastes the lines into Microsoft
Advertising: AdCopilot cannot.

## What this cannot see

Anything in Microsoft Advertising: the account, its campaigns, its spend, its
audiences, its approvals. Say so when the customer asks "how will it do on
Bing".

## Changes

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill reads Google Ads and writes nothing: every step in Microsoft Advertising is the customer's own click. Nothing is ever deleted. The numbers you give are the tool's numbers, never an invented one.

## Facts checked on 23 October 2026

From Microsoft's developer documentation on learn.microsoft.com: the import
options and their screen path in "Google Ads Import" and its option reference;
the responsive search ad limits in "Responsive Search Ads", the ad's data
object and "Entity Limits". Microsoft Advertising's own help pages could not be
opened by a tool on that day, so for what is and is not imported, its help
article is the referee.
