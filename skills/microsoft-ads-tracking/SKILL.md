---
name: microsoft-ads-tracking
description: "Check that Microsoft Advertising's UET tag (the Bing Ads tracking tag) is in Google Tag Manager, fires on the right pages and has conversion event tags behind it, and stage a missing tag as a draft for the customer to publish. Use when the user asks about the UET tag, Bing Ads or Microsoft Ads conversion tracking, a Microsoft Advertising tag that shows inactive or unverified, no conversions in Microsoft Ads, msclkid, or setting up a Microsoft conversion goal."
---

# Microsoft Ads tracking check

The customer wants to know whether Microsoft Advertising's tracking is set up on
their site: the UET tag (Universal Event Tracking, Microsoft's tracking tag),
the events behind it, and what is missing. You read their Google Tag Manager
through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`. You cannot
read their Microsoft Advertising account, so you work from what Tag Manager
shows and say what only Microsoft Advertising can tell them.

**Say this first, once.** Your first answer in this conversation opens with the
sentence below, in these words, and it is not repeated in later answers:

> Today AdCopilot checks your Microsoft Advertising UET tag in Google Tag Manager and stages tags there for you to publish, reports Bing traffic and key events in Google Analytics (GA4), finds UTM and auto-tagging gaps, guides conversion goal setup, prepares a Google Ads import from your Google Ads account, drafts responsive search ad copy and does the budget pacing math. It cannot read your Microsoft Advertising account yet: that part of AdCopilot is being built, and there is no date yet.

Call `get_org_context` with `source: "claude-plugin/adcopilot-microsoft-ads/0.1.2"`
first, before any other tool, unless you already called it in this
conversation. Send `source` exactly as written, the version
included. If this run is a scheduled task with nobody there to answer, send
`source: "claude-scheduled"` instead and change nothing. `get_org_context`'s
`next_step` and `playbook` describe the whole workspace, not this request: do
THIS request, keep any limit `next_step` adds, and offer the rest afterwards.

If Tag Manager is not connected, say what connecting it unlocks, in the
`unlocks` words `get_org_context` gives for it, and give the connect link
exactly as `get_org_context` returns it, never one from memory. Then stop: do not
guess what is in a container you cannot read. You may still offer to walk them
through Microsoft's UET Tag Helper below, which needs no connection.

## What you can and cannot see

You read with `gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`,
`gtm_list_tags`, `gtm_list_triggers` and `gtm_list_version_headers`. You write,
only on a yes, with `gtm_create_trigger` and `gtm_create_tag`.

- A workspace is a draft. A tag that sits in a workspace is on the site only if
  it was in a version someone published. `gtm_list_version_headers` lists the
  container's versions by number and name, with how many tags and triggers
  each holds. It gives no dates and not the tags inside a version, and it
  does not say which version is live. So never say a tag "is live" from a
  workspace read: say it is in the workspace, and send them to the proof in
  step 7.
- You cannot see the Microsoft Advertising account: whether the UET tag shows as
  active, which conversion goals exist, whether auto-tagging is on. The
  customer reads those in Microsoft Advertising, and you tell them what to look
  for.
- You cannot see code that is pasted straight into the site's pages instead of
  Tag Manager. Say so when the container has no UET tag: it may be there.

## The checks, in order

1. **Find the container that is on the site.** `gtm_list_accounts`, then
   `gtm_list_containers`, then `gtm_list_workspaces`. If there is more than one
   container, ask which one, by the name Tag Manager shows. Read the tags and
   triggers of the Default Workspace, and of the `AdCopilot` workspace if there
   is one: that is where AdCopilot stages its drafts.
2. **Find the UET tag.** In Tag Manager it is usually one of two things. Either a tag
   made from Microsoft's own UET template, which shows as a custom-template tag
   (a type other than `html`, at the time of writing) with the tag ID in its
   fields, or a Custom HTML tag (type `html`) whose code sets up a queue named
   `uetq`, loads a script from `bat.bing.com/bat.js` and carries the tag ID as
   `ti`. That is the shape in Microsoft's own example (checked 23 October 2026);
   Microsoft's code is the referee, so if the customer's code
   loads from a different Microsoft address, or looks different, say so and
   compare it with the code Microsoft Advertising gives them rather than
   calling it wrong. If it is neither, say what you see. Report: found or not, its name, its tag ID, whether it is
   paused, and whether a second tag carries the same ID.
3. **Where it fires.** Microsoft says to add the UET code to every page of the
   site. Read its trigger with `gtm_list_triggers`: All Pages, or something
   narrower that leaves pages out. Read any blocking trigger. Tag Manager's
   built-in triggers are not in what `gtm_list_triggers` returns: a firing
   trigger ID of `2147479553` is the built-in All Pages trigger (the
   connector's own tool text gives that ID, at the time of writing), and any
   other ID of 2147479000 or more is another built-in trigger, which you call
   built-in and let Tag Manager's own screen name. Never report a built-in
   trigger as missing. One UET tag can
   serve every conversion goal and audience, so a second tag with a different
   ID is not wrong by itself (Microsoft's own page, "Reasons for creating more
   than one UET tag", is the referee); the same code twice on one page is, and
   you cannot see that from Tag Manager alone, so the UET Tag Helper in step 7
   decides it.
4. **Consent.** Ask where their visitors are. For visitors in the European
   Economic Area, the United Kingdom and Switzerland, Microsoft says it
   enforces Consent Mode, with the default `denied`, and that conversions are
   lost if the `granted` signal is not passed when a visitor accepts. In the
   container, look for what passes it: a tag that sends `consent` and `update`
   with `ad_storage` to `uetq`, or the consent options of Microsoft's template
   ("Inherit initial consent" and "Enable consent updates", at the time of
   writing). Say what you found and that you cannot see their cookie banner. If
   nothing in the container passes consent and they have visitors there, that
   is a finding, with the fix in Microsoft's own page, "Setting up UET for
   consent mode".
5. **Events and goals.** Microsoft's UET tag records page visits and custom
   events, and counts nothing as a conversion until a conversion goal exists in
   Microsoft Advertising. Microsoft's goal types include (checked 23 October
   2026, in its API documentation): a URL (a page visited), an event, a
   duration, pages per visit, an app install or download, an offline
   conversion and an in-store transaction. Ask what the customer wants counted (a purchase, a lead, a call
   click). A thank-you page is a URL goal: the base tag on that page is enough,
   and no event tag is needed. A click or a form with no page of its own is an
   event goal: it needs an event tag in Tag Manager on a trigger shaped like
   the action, and an event is described by an action and, if wanted, a
   category, a label and a value. Read which UET event tags the container
   already has, by name and trigger, and list the actions that have none. The
   goals themselves, and their tracking status, are in Microsoft Advertising:
   tell them to look at the conversion goals page there. Microsoft names
   statuses such as Unverified, Tag inactive and No recent conversions
   (at the time of writing); each is a reason to run step 7.
6. **Click ID and UTM.** Microsoft's auto-tagging adds `msclkid`, a click ID of
   32 characters that is unique to each ad click, to the landing page address.
   It is an account setting in Microsoft Advertising, and Microsoft says that
   adding or changing a URL, event, duration, pages-per-visit or offline
   conversion goal switches it on. Its UTM tagging is a
   separate account setting, with three values in Microsoft's API: Inactive,
   Preserve and Replace. You cannot see either. Ask them to click one of their
   own ads and look for `msclkid` in the address bar of the landing page: a
   redirect that drops the query string would lose it. The Analytics side of this is
   the `microsoft-ads-traffic` skill.
7. **The proof that it fires.** Microsoft's UET Tag Helper is a browser
   extension for Edge and Chrome. It checks one page at a time: green means the
   tags work, yellow means they work but can improve, red means they are
   broken, and opening it shows the issue and the fix. Its badge number counts
   the UET requests the page sent, so a count higher than the page should send
   (one page load, plus any event on it) points to a tag firing twice. Tag Manager's own preview is the other referee for
   whether a trigger matches. Microsoft Advertising can take up to 24 hours to
   mark a new tag verified, so a tag set up today may show Unverified until
   tomorrow; if it is still Unverified or inactive after a day, the helper is
   where to look.

Give the answer in a few plain sentences: what is in the container, what is
missing, what only Microsoft Advertising can confirm, and the one next step.

## If there is no UET tag, or an event has no tag

Stage a tag only when the customer pastes the code. Microsoft Advertising gives
them the base code when they create a UET tag, and the code for an event when
they create an event goal. Never write UET code from memory and never edit what
they paste: stage it exactly as pasted. If they have none yet, tell them to
create the UET tag in Microsoft Advertising first (Microsoft's own page,
"Set up UET tags using Google Tag Manager", also covers Microsoft's template),
and wait.

Propose first, in one message: the tag as a Custom HTML tag named for what it
does ("Microsoft Ads UET base tag"), with the pasted code, firing on All Pages
(the built-in trigger; the connector's own tool text gives its ID as
`2147479553`, at the time of writing), or an event tag on a trigger you stage
first with `gtm_create_trigger` (a page-view trigger with a condition on the
page path, or whatever shape the action needs; read an existing trigger with
`gtm_list_triggers` to copy the shape Tag Manager uses). Say what it changes,
that it is staged in the `AdCopilot` workspace and not published, and how to
undo it: do not publish it, or discard it in Tag Manager. If they have
visitors in the European Economic Area, the United Kingdom or Switzerland,
say in the same message that step 4's consent finding applies to this tag
too. Make the call only after their yes. A Custom HTML tag takes the code in a parameter named `html`
(an existing `html` tag, as `gtm_list_tags` returns it, shows the keys it uses).

Then read it back with `gtm_list_tags` and `gtm_list_triggers`, give them the
Tag Manager link (`tagManagerUrl`) exactly as the server returns it with the
tag, and say that publishing is their click in Tag Manager (Submit, then
Publish, at the time of writing): nothing runs on the site until they do.
After they publish, send them to step 7. A trigger whose condition reads a
variable that is switched off in the container matches nothing, and Tag
Manager's preview shows it; switching a variable on is not part of this
check, so tell them to do it in Tag Manager if the preview says so.

## Changes

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. Tag Manager changes are staged in the `AdCopilot` workspace and never published. Nothing is ever deleted. The numbers and names you give are what the tools returned, never an invented one.

## Facts checked on 23 October 2026

From Microsoft's developer documentation on learn.microsoft.com: the UET code
(queue `uetq`, script `bat.bing.com/bat.js`, tag ID `ti`) and the consent
signal in "Setting up UET for consent mode"; Microsoft's UET template for Tag
Manager in "Google tag manager template - Consent mode"; the conversion goal
types in "Universal Event Tracking" and the ConversionGoalType reference;
`msclkid`, the goals that switch its auto-tagging on, and the UTM tagging
values in the Bulk and Customer Management reference. The UET Tag Helper's colours, badge and
24-hour note are from its store listing and from Microsoft's help pages as a
web search returned them. No tool could open Microsoft Advertising's own help
pages on that day, so where a screen's wording matters, Microsoft
Advertising's own screen is the referee.
