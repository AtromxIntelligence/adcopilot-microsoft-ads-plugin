---
description: "Review your Microsoft Advertising (Microsoft Ads, Bing Ads) account through AdCopilot: results, campaigns, search terms, conversion tracking, Microsoft's own recommendations and AdCopilot's checks, then offer the separate Clarity and Bing organic reports where your workspace has them."
---

Follow the `microsoft-advertising-review` skill. If the customer typed
something after the command, use it to choose the account, the campaign, the
check or the dates, and do not ask for it again: $ARGUMENTS

When the customer wants to know how visitors behave on their site, follow the
`microsoft-clarity` skill; when they want their site in Bing's organic search
results, follow the `bing-organic` skill. Each is a separate report, and each
reads only what `msads_get_context` says is offered and connected. For the UET
tag in Google Tag Manager, offer `/adcopilot-microsoft-ads:check`.

If `msads_get_context` is not among your tools, that proves nothing: the
client's tool list can be cached or out of date, so call it anyway and believe
what it says. If it cannot be called, the `ms` sign-in is not done: say so,
give the sign-in steps of `/adcopilot-microsoft-ads:setup`, and never describe
an account you did not read.
