---
name: setup
description: "Check the AdCopilot connector is connected and signed in, say what works today for Microsoft Ads (Bing Ads), and which Google products are connected."
---

Check that the AdCopilot connector is signed in, say plainly what this plugin
does for Microsoft Ads (Bing Ads) today and what it does not, and say which
Google products are connected.

Call `get_org_context` with `source: "claude-plugin/adcopilot-microsoft-ads/0.1.0"`
first, before any other tool. Send `source` exactly as written, the version
included. If this run is a scheduled task with nobody there to answer, send
`source: "claude-scheduled"` instead and change nothing. `get_org_context`'s
`next_step` and `playbook` describe the whole workspace, not this command: do
THIS command, keep any limit `next_step` adds, and offer the rest afterwards.

Open your first answer with this, in these words, once:

> Today AdCopilot checks your Microsoft Advertising UET tag in Google Tag Manager and stages tags there for you to publish, reports Bing traffic and key events in Google Analytics (GA4), finds UTM and auto-tagging gaps, guides conversion goal setup, prepares a Google Ads import from your Google Ads account, drafts responsive search ad copy and does the budget pacing math. It cannot read your Microsoft Advertising account yet: that comes when Microsoft approves AdCopilot's API access, and there is no date yet.

Then, from what `get_org_context` reports and nothing else:

- **Signed in.** If the call fails or the connector is missing, the customer
  signs in. In Claude Code, they run `/mcp`, choose `adcopilot` and sign in. In
  Claude on the web, in Cowork or in the desktop app, they open this plugin from
  the plugin list, then its Connectors tab, and Connect `adcopilot`. One
  connector and one sign-in serve every AdCopilot plugin they add. In Claude
  Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded
  first, and if Claude asks them to sign in again after they remove an AdCopilot
  plugin, they run `/mcp` and sign in once. Never offer "Add custom connector"
  to someone who has this plugin installed in Claude: the plugin already brings
  the connector.
- **Which Google products are connected.** For each of Google Tag Manager,
  Google Analytics 4 and Google Ads, say whether it is connected, what it
  unlocks for Microsoft Ads in one clause (Tag Manager: the UET tag check;
  Analytics: Bing traffic and key events; Google Ads: the import plan), and, for
  one that is not connected, the `unlocks` text and the connect link exactly as
  `get_org_context` returns them, never a link from memory. If the connector
  answers but reports nothing connected, that is the server working, not a
  fault: Google products are connected once inside AdCopilot, at
  `https://app.adcopilot.cloud`, not in this client.
- **What it will not do.** It reads no Microsoft Advertising account, and it
  changes nothing without an explicit yes.

End with the one next step that fits what is connected: `/adcopilot-microsoft-ads:check` when Tag Manager or
Analytics is connected, `/adcopilot-microsoft-ads:plan` when only Google Ads is,
and connecting one, with the link `get_org_context` gives, when none is.
