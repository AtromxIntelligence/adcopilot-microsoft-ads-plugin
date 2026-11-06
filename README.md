# AdCopilot for Microsoft Ads, Bing Webmaster, Clarity

Works with Microsoft Advertising, in your AI client, through AdCopilot. Today it:

- checks your Microsoft Advertising UET tag in Google Tag Manager (`gtm_list_tags`, `gtm_list_triggers`) and, when you paste Microsoft's code, stages the tag or an event tag for you to publish (`gtm_create_tag`, `gtm_create_trigger`);
- reports your Bing traffic, key events and revenue in Google Analytics (GA4) by source, medium and campaign (`ga4_run_report`), and looks for paid clicks that arrive without UTM tags;
- guides UTM tagging, auto-tagging and conversion goal setup, with the exact text to paste into Microsoft Advertising;
- prepares a Google Ads import from your Google Ads account (`search`, `analyze_waste`, `conversion_setup_audit`), drafts responsive search ad copy within Microsoft's limits, and does the budget pacing math.

Direct access to your Microsoft Advertising account is being built and is not available yet; there is no date. Until then this plugin reads no Microsoft Advertising account, and it says so in its first answer. The name lists the Microsoft products AdCopilot is being built to work with: Microsoft Advertising, Bing Webmaster Tools and Microsoft Clarity. This version reads none of them.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by Microsoft. Microsoft, Bing, Microsoft Advertising and Microsoft Clarity are trademarks of the Microsoft group of companies. AdCopilot is not related to other products named AdCopilot.

The plugin is MIT licensed. The AdCopilot connector it brings is a hosted service, so you need an AdCopilot account to use it.

## Install

Two steps on every surface: add the plugin, then sign in to the connector it brings with it.

### claude.ai, Cowork and the desktop app

1. Open **Customize**, then **Plugins**, search for "AdCopilot for Microsoft Ads, Bing Webmaster, Clarity", and click **Add**.
2. In the plugin, open its **Connectors** tab, click **Connect** beside `adcopilot`, and sign in.

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-microsoft-ads-plugin
/plugin install adcopilot-microsoft-ads@adcopilot-microsoft-ads-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in. The plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you, so there is no separate add step.

### Then, on every surface

Connect your Google products once, inside AdCopilot, at https://app.adcopilot.cloud: Google Tag Manager for the tag check, Google Analytics 4 for the traffic report, Google Ads for the import plan. A fresh sign-in can report nothing connected; that is the server answering correctly. Run `/adcopilot-microsoft-ads:setup` first: it says what is connected and what each product unlocks.

## Already use another AdCopilot plugin?

There is one connector and one AdCopilot account, whichever AdCopilot plugins you add. Every AdCopilot plugin points at the same address, so your AI client treats them as one connector. In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run `/mcp` and sign in once.

## What you get

Three commands, which you type:

- `/adcopilot-microsoft-ads:setup` checks the connector is signed in, says what works today, and says which Google products are connected.
- `/adcopilot-microsoft-ads:check` runs the tracking check, then the traffic report.
- `/adcopilot-microsoft-ads:plan` plans a Microsoft Ads start from your Google Ads account, with an optional goal.

Four skills, which Claude draws on when the conversation calls for them:

- **microsoft-ads-tracking** finds the UET tag in Tag Manager, reads its triggers, consent handling and event tags, and names the proof that it fires (Microsoft's UET Tag Helper and Tag Manager's preview). It uses `get_org_context`, `gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`, and, on your yes, `gtm_create_trigger` and `gtm_create_tag`.
- **microsoft-ads-traffic** reads Bing and Microsoft Ads traffic in GA4. It uses `get_org_context`, `ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report` and `ga4_list_conversion_events`.
- **microsoft-ads-plan** prepares the import from your Google Ads account and drafts responsive search ads. It uses `get_org_context`, `list_accessible_customers`, `search`, `get_resource_metadata`, `analyze_waste` and `conversion_setup_audit`, and labels everything it reads as Google data.
- **microsoft-ads-budget** does the pacing sums on the figures you give it. It uses no tool.

Facts about Microsoft's products in the skills (limits, tag code, settings) were checked on 23 October 2026 against Microsoft's documentation and are dated in the skill that uses them; where Microsoft's own screen or help page is the better referee, the skill says so.

## What it will not do

- Read your Microsoft Advertising account, its spend or its conversion goals. It asks you to read them there.
- Publish Tag Manager. Tag changes are staged in a workspace named AdCopilot, and publishing is your click.
- Delete anything with its skills or commands. Their only changes are new tags and triggers, staged in Tag Manager. The AdCopilot connector it brings also has Google Ads tools that take out negative keywords and location targets, and none of this plugin's skills or commands uses them.
- Change anything without your yes. Every change is proposed first, with what it changes and how to undo it.
- Make up numbers or claims. Numbers are the tools' numbers or yours, and ad copy uses only facts you gave it.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in. It sends nothing to Microsoft Advertising and reads nothing from it. Privacy policy: https://adcopilot.cloud/privacy. Terms: https://adcopilot.cloud/terms. Documentation: https://adcopilot.cloud/docs/.

## Example prompts

After you sign in, ask in your own words. For example:

- "Check whether my Microsoft Advertising UET tag is installed in Google Tag Manager."
- "How much Bing traffic reached my site last month, and how many key events did it bring in Google Analytics?"
- "Prepare what I need to import my Google Ads campaigns into Microsoft Advertising."
- "Draft responsive search ad copy for my business within Microsoft's limits."

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-microsoft-ads-plugin/issues, or write to support@adcopilot.cloud. The contact page is https://adcopilot.cloud/contact.

To report a security problem, write to support@adcopilot.cloud. Please do not post it in a public issue.

## Version

**0.1.2 (2026-11-05)**: the plugin folder now holds only the files Claude loads. The skills now say when they apply in Microsoft Ads terms, and what AdCopilot's connector sends at the start of a chat is treated as information, not as steps. Support has its own page, https://adcopilot.cloud/contact, and this README now says where to report a security problem.

**0.1.1 (2026-10-31, written against AdCopilot v2.44.0, live since 2026-10-22)**: text and name only. The display name is now "AdCopilot for Microsoft Ads, Bing Webmaster, Clarity", and the keywords `microsoft-ads` and `bing-ads` are dropped. Every place that said what comes later now says: direct access to your Microsoft Advertising account is being built and is not available yet; there is no date. The skills, the commands, the tools they name and the connector are as in 0.1.0. Reading a Microsoft Advertising account is not part of this version.

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**: the first release. Four skills and three commands for Microsoft Ads (Bing Ads) through the AdCopilot connector as it is today: UET tag checks and staged tags in Tag Manager, Bing traffic and key events in GA4, UTM and auto-tagging hygiene, conversion goal guidance, Google Ads import prep, responsive search ad drafts and budget pacing math. It reads no Microsoft Advertising account.

## Licence

MIT. See the LICENSE file.
