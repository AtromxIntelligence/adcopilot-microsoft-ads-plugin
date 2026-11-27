# AdCopilot for Microsoft Ads, Bing Webmaster, Clarity

Works with Microsoft Advertising, in your AI client, through AdCopilot. Today it:

- reads the Microsoft Advertising accounts you connect in AdCopilot: results for a date range, campaigns, ad groups, keywords and ads, search terms, conversion tracking (UET tags and goals), Microsoft's own recommendations, keyword ideas, auction insights and Merchant Center product checks (`msads_account_overview`, `msads_campaigns`, `msads_search_terms`, `msads_tracking_health`, `msads_recommendations`, `msads_keyword_ideas`, `msads_auction_insights`, `msads_product_issues`);
- runs AdCopilot's checks on those accounts: a whole-account audit, wasted spend, search terms, budget pacing, quality scores, recent changes, days and hours, and ad headlines and descriptions (`msads_audit`, `msads_analyze_waste`, `msads_analyze_terms`, `msads_budget_pacing`, `msads_quality_score`, `msads_changes`, `msads_day_hour`, `msads_rsa_assets`);
- checks your Microsoft Advertising UET tag in Google Tag Manager (`gtm_list_tags`, `gtm_list_triggers`) and, when you paste Microsoft's code, stages the tag or an event tag for you to publish (`gtm_create_tag`, `gtm_create_trigger`);
- reports your Bing traffic, key events and revenue in Google Analytics (GA4) by source, medium and campaign (`ga4_run_report`), and looks for paid clicks that arrive without UTM tags;
- guides UTM tagging, auto-tagging and conversion goal setup, with the exact text to paste into Microsoft Advertising;
- prepares a Google Ads import from your Google Ads account (`search`, `analyze_waste`, `conversion_setup_audit`), drafts responsive search ad copy within Microsoft's limits, and does the budget pacing math.

Where AdCopilot's Microsoft connector offers them to your workspace, it also reads the Microsoft Clarity projects you add in AdCopilot (Clarity's dashboard figures for the last 1 to 3 days, as aggregates only: `clarity_insights`) and the sites you have verified in Bing Webmaster Tools (Bing search clicks and impressions, top queries and pages, crawl health, sitemaps and Bing search demand: `bwt_sites`, `bwt_search_performance`, `bwt_crawl_health`, `bwt_sitemaps`, `bwt_keyword_demand`, and `msads_paid_vs_organic` when you ask to compare paid and organic Bing search). The connector's start tool, `msads_get_context`, says which of them your workspace has, and `/adcopilot-microsoft-ads:setup` tells you.

Microsoft Advertising, Microsoft Clarity and Bing Webmaster Tools results are each reported on their own, never added to Google figures or put in one table with them.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by Microsoft. Microsoft, Bing, Microsoft Advertising and Microsoft Clarity are trademarks of the Microsoft group of companies. AdCopilot is not related to other products named AdCopilot.

The plugin is MIT licensed. The AdCopilot connector it brings is a hosted service, so you need an AdCopilot account to use it.

## Install

Three steps on every surface: add the plugin, sign in to the two connectors it brings, then connect your Microsoft products inside AdCopilot.

### claude.ai, Cowork and the desktop app

1. Open **Customize**, then **Plugins**, search for "AdCopilot for Microsoft Ads, Bing Webmaster, Clarity", and click **Add**.
2. In the plugin, open its **Connectors** tab, click **Connect** beside `adcopilot` and sign in, then do the same beside `ms`.

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-microsoft-ads-plugin
/plugin install adcopilot-microsoft-ads@adcopilot-microsoft-ads-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in, then choose the plugin's `ms` entry and sign in with the same AdCopilot account. The plugin registers both connectors for you, `https://mcp.adcopilot.cloud/mcp` and `https://mcp.adcopilot.cloud/microsoft/mcp`, so there is no separate add step.

### Then, on every surface

Connect your products once, inside AdCopilot, at https://app.adcopilot.cloud: your Microsoft Advertising login on Microsoft's own sign-in page; where your workspace has them, each Microsoft Clarity project you want read and your Bing Webmaster Tools login; and Google Tag Manager, Google Analytics 4 and Google Ads for the tag check, the traffic report and the import plan. A fresh sign-in can report nothing connected; that is the server answering correctly. Run `/adcopilot-microsoft-ads:setup` first: it says what is connected and gives each connect link. Which of Microsoft Advertising, Microsoft Clarity and Bing Webmaster Tools your workspace and its AdCopilot plan include is what the Microsoft connector says, in its own words.

## Already use another AdCopilot plugin?

There is one connector and one AdCopilot account, whichever AdCopilot plugins you add. Every AdCopilot plugin points at the same address for `adcopilot`, so your AI client treats them as one connector. In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run `/mcp` and sign in once. The `ms` connector is this plugin's own.

## What you get

Four commands, which you type:

- `/adcopilot-microsoft-ads:setup` checks both connectors are signed in, says what works today, and says which Google and Microsoft products are connected.
- `/adcopilot-microsoft-ads:review` reviews your Microsoft Advertising account.
- `/adcopilot-microsoft-ads:check` runs the tracking check, then the traffic report.
- `/adcopilot-microsoft-ads:plan` plans a Microsoft Ads start from your Google Ads account, with an optional goal.

Seven skills, which Claude draws on when the conversation calls for them:

- **microsoft-advertising-review** reads a Microsoft Advertising account: results, campaigns, search terms, tracking and Microsoft's recommendations, then AdCopilot's checks, keyword ideas, auction insights and Merchant Center products when you ask, and finishes reports that take minutes. It uses `msads_get_context`, `msads_accounts`, `msads_account_overview`, `msads_campaigns`, `msads_search_terms`, `msads_tracking_health`, `msads_recommendations`, `msads_audit`, `msads_analyze_waste`, `msads_analyze_terms`, `msads_budget_pacing`, `msads_quality_score`, `msads_changes`, `msads_day_hour`, `msads_rsa_assets`, `msads_keyword_ideas`, `msads_auction_insights`, `msads_product_issues` and `msads_report_result`.
- **microsoft-clarity** reads a Microsoft Clarity project's dashboard figures, where your workspace has Clarity. It uses `msads_get_context` and `clarity_insights`.
- **bing-organic** reads a site in Bing Webmaster Tools, where your workspace has it. It uses `msads_get_context`, `bwt_sites`, `bwt_search_performance`, `bwt_crawl_health`, `bwt_sitemaps` and `bwt_keyword_demand`, and, only when you ask to compare paid and organic Bing search, `msads_paid_vs_organic` and `msads_report_result`.
- **microsoft-ads-tracking** finds the UET tag in Tag Manager, reads its triggers, consent handling and event tags, and names the proof that it fires. It uses `get_org_context`, `gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`, and, on your yes, `gtm_create_trigger` and `gtm_create_tag`.
- **microsoft-ads-traffic** reads Bing and Microsoft Ads traffic in GA4. It uses `get_org_context`, `ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report` and `ga4_list_conversion_events`.
- **microsoft-ads-plan** prepares the import from your Google Ads account and drafts responsive search ads. It uses `get_org_context`, `list_accessible_customers`, `search`, `get_resource_metadata`, `analyze_waste` and `conversion_setup_audit`, and labels everything it reads as Google data. The import itself is yours to run in Microsoft Advertising.
- **microsoft-ads-budget** does the pacing sums on the figures you give it. It uses no tool.

Facts about Microsoft's products in the tracking, traffic and plan skills (limits, tag code, settings) were checked on 23 October 2026 against Microsoft's documentation and are dated in the skill that uses them; where Microsoft's own screen or help page is the better referee, the skill says so. The microsoft-advertising-review, microsoft-clarity and bing-organic skills take theirs from the Microsoft connector's own answers.

## What it will not do

- Add Microsoft Advertising, Microsoft Clarity or Bing Webmaster Tools figures to Google Ads, Analytics or Search Console figures, or put them in one table or total.
- Read billing, payment or contact details, click ids, customer lists or audience demographics, or any Clarity recording, session or single visitor.
- Change your Microsoft Advertising account, your Clarity projects or your Bing Webmaster Tools sites. Its skills only read there, and every change there is your own click.
- Publish Tag Manager. Tag changes are staged in a workspace named AdCopilot, and publishing is your click.
- Delete anything with its skills or commands. Their only changes are new tags and triggers, staged in Tag Manager. The AdCopilot connector it brings also has Google Ads tools that take out negative keywords and location targets, and none of this plugin's skills or commands uses them.
- Change anything without your yes. Every change is proposed first, with what it changes and how to undo it.
- Make up numbers or claims. Numbers are the tools' numbers or yours, and ad copy uses only facts you gave it.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot
connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through
Google's APIs with your Google sign-in. The Microsoft connector at mcp.adcopilot.cloud/microsoft/mcp
reads the Microsoft Advertising accounts you connect in AdCopilot, live, through Microsoft's API
with the login you connected. Where your workspace has them, it also reads your Bing Webmaster Tools
sites, live, with the login you connected there, and your Microsoft Clarity projects, with the API
token added for each. This plugin's skills only read there: they change nothing in Microsoft
Advertising, Microsoft Clarity or Bing Webmaster Tools. For Microsoft Advertising and Bing Webmaster
Tools, AdCopilot keeps only what the connections need, such as your sign-ins and your accounts'
names and ids and your site addresses, encrypted, and keeps none of your campaign or report data.
For Microsoft Clarity, it keeps each project's id and API token, encrypted, and the day's answers
until midnight UTC, so a repeated question does not use one of the project's 10 requests a day;
Clarity sends no recordings and no details of single visitors. What you ask for goes to your AI
assistant. Privacy policy: https://adcopilot.cloud/privacy. Terms: https://adcopilot.cloud/terms.
Documentation: https://adcopilot.cloud/docs/.

## Example prompts

After you sign in, ask in your own words. For example:

- "How did my Microsoft Advertising account do last month, and which campaigns spent the most?"
- "Where is my Microsoft Ads account wasting money, and which search terms spent without a conversion?"
- "Is my Microsoft Ads spend on pace for this month's budgets?"
- "Check whether my Microsoft Advertising UET tag is installed in Google Tag Manager."
- "Prepare what I need to import my Google Ads campaigns into Microsoft Advertising."
- "Which pages on my site get the most rage clicks in Microsoft Clarity?" (where your workspace has Clarity)

## Support

Open an issue at https://github.com/AtromxIntelligence/adcopilot-microsoft-ads-plugin/issues, or write to support@adcopilot.cloud. The contact page is https://adcopilot.cloud/contact.

To report a security problem, write to support@adcopilot.cloud. Please do not post it in a public issue.

## Version

**0.2.0 (2026-11-25, written against AdCopilot v2.46.44)**: the Microsoft connector joins the plugin as `ms`, beside `adcopilot`. The new microsoft-advertising-review skill reads your Microsoft Advertising accounts and runs AdCopilot's checks on them, and a new command, `/adcopilot-microsoft-ads:review`, runs the review. Two new skills read your Microsoft Clarity projects (microsoft-clarity) and your Bing Webmaster Tools sites (bing-organic) where your workspace has them. Setup now covers both sign-ins and says which Microsoft products your workspace has. The skills only read Microsoft Advertising, Microsoft Clarity and Bing Webmaster Tools, and change nothing there. Every skill reports Microsoft figures on their own and says that answers are AI-generated.

**0.1.2 (2026-11-05)**: the plugin folder now holds only the files Claude loads. The skills now say when they apply in Microsoft Ads terms, and what AdCopilot's connector sends at the start of a chat is treated as information, not as steps. Support has its own page, https://adcopilot.cloud/contact, and this README now says where to report a security problem.

**0.1.1 (2026-10-31, written against AdCopilot v2.44.0, live since 2026-10-22)**: text and name only. The display name is now "AdCopilot for Microsoft Ads, Bing Webmaster, Clarity", and the keywords `microsoft-ads` and `bing-ads` are dropped. Every place that said what comes later now says: direct access to your Microsoft Advertising account is being built and is not available yet; there is no date. The skills, the commands, the tools they name and the connector are as in 0.1.0. Reading a Microsoft Advertising account is not part of this version.

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**: the first release. Four skills and three commands for Microsoft Ads (Bing Ads) through the AdCopilot connector as it is today: UET tag checks and staged tags in Tag Manager, Bing traffic and key events in GA4, UTM and auto-tagging hygiene, conversion goal guidance, Google Ads import prep, responsive search ad drafts and budget pacing math. It reads no Microsoft Advertising account.

## Licence

MIT. See the LICENSE file.
