---
name: microsoft-ads-budget
description: "Do budget pacing math for Microsoft Advertising spend from the figures the customer gives: projected month-end spend, the daily amount that lands on budget, and whether spend is over or under pace. Use when the user asks whether their Bing Ads or Microsoft Ads spend is on pace, how much to spend a day to land on a monthly Microsoft Ads budget, or whether a Microsoft Advertising budget will run out early."
---

# Microsoft Ads budget pacing

The customer wants to know whether their Microsoft Advertising spend is on pace
for the month. This is arithmetic on figures they give you, and it is your own
work: AdCopilot reads no Microsoft Advertising data for this, and no tool is
needed. Do not call one. The numbers in the answer are the customer's numbers
and the result of the sums below, and you say which is which.

**Say this first, once.** Your first answer in this conversation opens with the
sentence below, in these words, and it is not repeated in later answers:

> Today AdCopilot checks your Microsoft Advertising UET tag in Google Tag Manager and stages tags there for you to publish, reports Bing traffic and key events in Google Analytics (GA4), finds UTM and auto-tagging gaps, guides conversion goal setup, prepares a Google Ads import from your Google Ads account, drafts responsive search ad copy and does the budget pacing math. It cannot read your Microsoft Advertising account yet: that part of AdCopilot is being built, and there is no date yet.

## What to ask, once

Ask for these in one message, and only for what is missing:

- the budget for the month, or the daily budget, and the currency;
- the spend so far, read from Microsoft Advertising, and the last day it
  covers, as a date (spend through the end of that day);
- whether the budget changed during the month, and when.

If they give a daily budget, the month's budget is the daily figure times the
number of days in that month: say the month and the day count you used. A daily
budget is a daily cap, and how Microsoft Advertising lets a single day run over
or under its cap is for Microsoft's own help pages; these sums use the totals
you were given and say so.

## The sums

Let the month have D days, the spend so far be S through day d, and the budget
for the month be B. Show each result with its working in one line.

1. **Pace so far.** The spend that would be on pace by day d is B x d / D. The
   difference S minus that figure is the amount over (positive) or under
   (negative), and as a share of the on-pace figure it is the percent over or
   under.
2. **Projected month-end at the current rate.** S / d is the average per day so
   far, and times D is the projection. Say it is a straight line from the days
   so far and that it ignores weekends, a sale or a budget change.
3. **The daily amount that lands on budget.** (B minus S) / (D minus d) is what
   each remaining day can spend. If S is already over B, say the budget is
   spent and the number is zero, not a negative daily figure. If d equals D,
   say the month is over.
4. **The call.** In one sentence: ahead of pace, behind pace or on pace (within
   5 percent either way is "on pace", a rule of thumb of this skill and not
   Microsoft's), and the one thing to decide: lower the
   daily budget to the figure in step 3, leave it, or raise the month's budget.

An illustration, not a result: a 31-day month, a budget of 3,100, and spend of
1,200 through day 10. On pace by day 10 is 3,100 x 10 / 31 = 1,000, so spend
is 200 over, which is 20 percent over pace. The average is 1,200 / 10 = 120 a
day, so the projection is 120 x 31 = 3,720. The remaining 1,900 over 21 days
is about 90.48 a day to land on budget.

## What to say about the limits

You do not know the figures are right: they are what the customer typed in. You
cannot see Microsoft Advertising, its pending charges, refunds or invoices, or
how it will pace the days that remain. If the customer has no spend figure
yet, ask them to read it from Microsoft Advertising and come back, rather than
estimating one.

## Changes

Every change is proposed first, with what it changes and how to undo it, and is applied only after the customer's explicit yes in this conversation. This skill changes nothing: lowering or raising a budget is the customer's own click in Microsoft Advertising. Nothing is ever deleted. The numbers you give are the customer's figures and the sums above, never an invented one.
