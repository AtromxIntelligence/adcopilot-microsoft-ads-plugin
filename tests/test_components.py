"""The skills, the commands and the README, held to what the connector really has.

The plugin makes claims the directory and the customer both rely on: that it
uses only tools the AdCopilot connector serves, that it never reads a Microsoft
Advertising account, that every change waits for a yes, and that the first
answer says what works today and what comes later. This file holds the text to
each of them, with the standard library only, and no test reads an
environment variable.

Run with `python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILLS = ["microsoft-ads-tracking", "microsoft-ads-traffic", "microsoft-ads-plan",
          "microsoft-ads-budget"]
COMMANDS = ["setup", "check", "plan"]

# The tools each skill and command may name, by bare name. The budget skill
# names none: its sums are the model's own, and it must not call anything.
ALLOWED = {
    "skills/microsoft-ads-tracking/SKILL.md": {
        "get_org_context", "gtm_list_accounts", "gtm_list_containers",
        "gtm_list_workspaces", "gtm_list_tags", "gtm_list_triggers",
        "gtm_list_version_headers", "gtm_create_trigger", "gtm_create_tag"},
    "skills/microsoft-ads-traffic/SKILL.md": {
        "get_org_context", "ga4_list_account_summaries", "ga4_get_metadata",
        "ga4_run_report", "ga4_list_conversion_events"},
    "skills/microsoft-ads-plan/SKILL.md": {
        "get_org_context", "list_accessible_customers", "search",
        "get_resource_metadata", "analyze_waste", "conversion_setup_audit"},
    "skills/microsoft-ads-budget/SKILL.md": set(),
    "commands/setup.md": {"get_org_context"},
    "commands/check.md": {"get_org_context"},
    "commands/plan.md": set(),
}

# The first answer of every skill, and /setup, says this once. It is one line
# in the files so that it can be compared as written.
TODAY_LATER = (
    "Today AdCopilot checks your Microsoft Advertising UET tag in Google Tag "
    "Manager and stages tags there for you to publish, reports Bing traffic and "
    "key events in Google Analytics (GA4), finds UTM and auto-tagging gaps, "
    "guides conversion goal setup, prepares a Google Ads import from your Google "
    "Ads account, drafts responsive search ad copy and does the budget pacing "
    "math. It cannot read your Microsoft Advertising account yet: that comes "
    "when Microsoft approves AdCopilot's API access, and there is no date yet."
)

APPROVAL = (
    "Every change is proposed first, with what it changes and how to undo it, "
    "and is applied only after the customer's explicit yes in this conversation."
)

TRADEMARK_LINE = (
    "Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with "
    "or endorsed by Microsoft. Microsoft, Microsoft Advertising and Bing are "
    "trademarks of Microsoft Corporation."
)

# Tools that are in the registry but switched off in production: never named.
SWITCHED_OFF = ("shopping_product_issues", "lsa_leads", "lsa_rate_lead")

# A backticked snake_case word is treated as a tool name when it starts with
# one of these. Words such as `ad_storage` or a UTM parameter are not.
TOOL_PREFIXES = ("gsc_", "ga4_", "gtm_", "create_", "add_", "set_", "update_",
                 "remove_", "list_", "get_", "run_", "analyze_", "pause_",
                 "attach_", "link_", "submit_", "request_", "inspect_",
                 "enable_", "save_", "keyword_", "quality_", "bidding_",
                 "budget_", "conversion_", "explain_", "paid_", "rsa_",
                 "account_", "change_", "day_of_", "full_")
SNAKE_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)+$")
BACKTICK_RE = re.compile(r"`([^`\n]+)`")


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def squash(text):
    """Whitespace collapsed to single spaces, so a wrapped line still compares."""
    return re.sub(r"\s+", " ", text).strip()


def connector_tools():
    names = set()
    for line in read("tests/connector_tools.txt").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            names.add(line)
    return names


def front_matter(rel):
    """(fields, body) of a skill or command. Fields are `key: value` lines only:
    a list, a block or a continuation line is refused, because the description
    must be one string of text."""
    text = read(rel)
    if not text.startswith("---\n"):
        raise AssertionError("%s has no front matter" % rel)
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError("%s front matter is not closed" % rel)
    fields = {}
    for line in text[4:end].split("\n"):
        m = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):[ ]+(\S.*)$", line)
        if not m:
            raise AssertionError("%s front matter line is not `key: value`: %r" % (rel, line))
        key, value = m.group(1), m.group(2).strip()
        if value[0] in "[{|>&*!-":
            raise AssertionError("%s: %s must be a plain text value, not a list or block" % (rel, key))
        if value[0] in "\"'":
            quote = value[0]
            if len(value) < 2 or value[-1] != quote or quote in value[1:-1] or "\\" in value:
                raise AssertionError("%s: %s has an unterminated or escaped quote" % (rel, key))
            value = value[1:-1]
        fields[key] = value
    return fields, text[end + 5:]


def component_files():
    files = ["skills/%s/SKILL.md" % s for s in SKILLS] + ["commands/%s.md" % c for c in COMMANDS]
    return files


def prose_without_code_fences(text):
    out, fenced = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return "\n".join(out)


class Components(unittest.TestCase):

    def test_the_skills_and_commands_are_exactly_the_decided_ones(self):
        skills = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
        self.assertEqual(skills, sorted(SKILLS))
        commands = sorted(p.stem for p in (ROOT / "commands").glob("*.md"))
        self.assertEqual(commands, sorted(COMMANDS))
        for forbidden in ("agents", "hooks", "bin", "evals"):
            self.assertFalse((ROOT / forbidden).exists(), forbidden + "/ is not part of 0.1.0")

    def test_front_matter_parses_with_a_name_and_one_text_description(self):
        for rel in component_files():
            fields, _body = front_matter(rel)
            self.assertEqual(sorted(fields), ["description", "name"], rel)
            stem = Path(rel).parent.name if rel.endswith("SKILL.md") else Path(rel).stem
            self.assertEqual(fields["name"], stem, rel)
            self.assertIsInstance(fields["description"], str)
            self.assertGreater(len(fields["description"].strip()), 40, rel)
            self.assertLessEqual(len(fields["description"]), 1024, rel)

    def test_a_skill_description_says_when_to_use_it(self):
        for skill in SKILLS:
            fields, _ = front_matter("skills/%s/SKILL.md" % skill)
            self.assertIn("Use when the user asks", fields["description"], skill)

    def test_tool_names_are_the_connectors_real_ones_and_each_file_names_only_its_own(self):
        tools = connector_tools()
        self.assertEqual(len(tools), 118)
        for forbidden in SWITCHED_OFF:
            self.assertNotIn(forbidden, tools)
        for rel, allowed in ALLOWED.items():
            self.assertTrue(allowed <= tools, "%s allows a tool the connector lacks: %s"
                            % (rel, sorted(allowed - tools)))
            for token in BACKTICK_RE.findall(read(rel)):
                token = token.strip()
                if token in tools:
                    self.assertIn(token, allowed, "%s names `%s`, which it does not use" % (rel, token))
                elif SNAKE_RE.match(token) and token.startswith(TOOL_PREFIXES):
                    self.fail("%s names `%s`, which is not a tool the connector serves" % (rel, token))
        for rel in component_files() + ["README.md"]:
            text = read(rel)
            for forbidden in SWITCHED_OFF:
                self.assertNotIn(forbidden, text, rel)

    def test_the_readme_names_only_real_tools(self):
        tools = connector_tools()
        union = set().union(*ALLOWED.values())
        for token in BACKTICK_RE.findall(read("README.md")):
            token = token.strip()
            if SNAKE_RE.match(token) and token.startswith(TOOL_PREFIXES):
                self.assertIn(token, tools, "README names `%s`" % token)
            if token in tools:
                self.assertIn(token, union, "README names `%s`, which no skill uses" % token)

    def test_no_namespaced_tool_name_appears_anywhere(self):
        # The namespace belongs to whichever AdCopilot plugin loaded first, so
        # a skill must name a tool by its bare name.
        # Built by joining two halves, so this file does not contain the
        # prefix it looks for.
        prefix = "mcp" + "__"
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or "__pycache__" in path.parts or not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue  # the icon
            self.assertNotIn(prefix, text, str(path))

    def test_every_get_org_context_call_carries_this_plugins_marker(self):
        version = json.loads(read(".claude-plugin/plugin.json"))["version"]
        marker = "claude-plugin/adcopilot-microsoft-ads/%s" % version
        for rel in component_files():
            text = read(rel)
            sources = re.findall(r'source:\s*"([^"]*)"', text)
            for value in sources:
                self.assertIn(value, (marker, "claude-scheduled"), "%s sends source %r" % (rel, value))
            self.assertNotIn("claude-plugin/%s" % version, text.replace(marker, ""), rel)
            if ALLOWED[rel] and "get_org_context" in ALLOWED[rel] and rel not in (
                    "commands/check.md",):
                self.assertIn('source: "%s"' % marker, text, rel)
                self.assertIn('source: "claude-scheduled"', text, rel)
                self.assertIn("next_step", text, rel)
                self.assertIn("playbook", text, rel)
            if not ALLOWED[rel]:
                self.assertEqual(sources, [], rel)

    def test_every_skill_holds_the_approval_paragraph(self):
        for skill in SKILLS:
            self.assertIn(APPROVAL, squash(read("skills/%s/SKILL.md" % skill)), skill)

    def test_every_skill_and_setup_says_what_works_today_and_what_comes_later(self):
        for rel in ["skills/%s/SKILL.md" % s for s in SKILLS] + ["commands/setup.md"]:
            self.assertIn(TODAY_LATER, squash(read(rel)), rel)
            # Once, and as the first answer.
            self.assertEqual(squash(read(rel)).count(TODAY_LATER), 1, rel)

    def test_a_product_that_is_not_connected_is_answered_from_the_servers_words(self):
        for skill in ("microsoft-ads-tracking", "microsoft-ads-traffic", "microsoft-ads-plan"):
            text = squash(read("skills/%s/SKILL.md" % skill))
            self.assertIn("`unlocks` words", text, skill)
            self.assertIn("exactly as `get_org_context` returns", text, skill)
        self.assertIn("`unlocks` text and the connect link exactly as `get_org_context` returns", squash(read("commands/setup.md")))

    def test_no_skill_pretends_to_read_a_microsoft_advertising_account(self):
        plan = squash(read("skills/microsoft-ads-plan/SKILL.md"))
        self.assertIn("AdCopilot reads no Microsoft Advertising data for this", plan)
        budget = squash(read("skills/microsoft-ads-budget/SKILL.md"))
        self.assertIn("AdCopilot reads no Microsoft Advertising data for this", budget)
        self.assertIn("no tool is needed. Do not call one.", budget)
        self.assertIn("You cannot read their Microsoft Advertising account",
                      squash(read("skills/microsoft-ads-tracking/SKILL.md")))
        self.assertIn("You cannot read their Microsoft Advertising account",
                      squash(read("skills/microsoft-ads-traffic/SKILL.md")))

    def test_tag_manager_changes_are_staged_and_never_published(self):
        text = squash(read("skills/microsoft-ads-tracking/SKILL.md"))
        self.assertIn("staged in the `AdCopilot` workspace and never published", text)
        self.assertIn("Nothing is ever deleted.", text)
        self.assertIn("publishing is their click in Tag Manager", text)
        # It stages only the code the customer pastes, never code from memory.
        self.assertIn("Stage a tag only when the customer pastes the code.", text)
        self.assertIn("Never write UET code from memory", text)

    def test_microsoft_facts_are_dated(self):
        for skill in ("microsoft-ads-tracking", "microsoft-ads-traffic", "microsoft-ads-plan"):
            text = read("skills/%s/SKILL.md" % skill)
            self.assertIn("23 October 2026", text, skill)
            self.assertIn("referee", text, skill)

    def test_the_commands_point_at_their_skills(self):
        self.assertIn("`microsoft-ads-tracking` skill", read("commands/check.md"))
        self.assertIn("`microsoft-ads-traffic`", read("commands/check.md"))
        plan = read("commands/plan.md")
        self.assertIn("`microsoft-ads-plan` skill", plan)
        self.assertIn("$ARGUMENTS", plan)


class Readme(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = read("README.md")

    def test_it_is_long_enough_for_the_directory_and_not_a_wall(self):
        prose = prose_without_code_fences(self.text)
        words = len(re.findall(r"\S+", prose))
        self.assertGreaterEqual(words, 40)
        self.assertGreaterEqual(words, 600)
        self.assertLessEqual(words, 1200)

    def test_it_opens_with_the_display_name(self):
        self.assertTrue(self.text.startswith("# AdCopilot for Microsoft Ads (Bing Ads)\n"))

    def test_it_holds_the_trademark_line_and_the_plans_line(self):
        text = squash(self.text)
        self.assertIn(TRADEMARK_LINE, text)
        self.assertIn("AdCopilot is not related to other products named AdCopilot.", text)
        self.assertIn("The plugin is free (MIT). The AdCopilot connector is a hosted service: "
                      "Free plan available; paid plans on https://adcopilot.cloud/pricing", text)

    def test_it_says_today_and_later_in_the_first_lines(self):
        head = squash("\n".join(self.text.split("\n")[:12]))
        self.assertIn("Today it:", head)
        self.assertIn("Direct access to your Microsoft Advertising account comes when Microsoft "
                      "approves AdCopilot's API access; there is no date yet.", head)

    def test_it_explains_install_on_every_surface_and_the_shared_connector(self):
        text = squash(self.text)
        for needle in (
                "Customize", "Plugins", "Connectors", "Connect",
                "/plugin marketplace add AtromxIntelligence/adcopilot-microsoft-ads-plugin",
                "/plugin install adcopilot-microsoft-ads@adcopilot-microsoft-ads-plugin",
                "/mcp", "https://app.adcopilot.cloud",
                "Already use another AdCopilot plugin?",
                "One connector, one sign-in, whichever AdCopilot plugins you add.",
                "`/mcp` shows the connector once, under whichever AdCopilot plugin loaded first.",
                "If Claude asks you to sign in again after you remove an AdCopilot plugin, run `/mcp` and sign in once."):
            self.assertIn(needle, text, needle)

    def test_it_says_what_it_will_not_do(self):
        text = squash(self.text)
        for needle in ("## What it will not do", "Read your Microsoft Advertising account",
                       "Publish Tag Manager.", "Delete anything.",
                       "Change anything without your yes."):
            self.assertIn(needle, text, needle)

    def test_it_discloses_where_data_goes(self):
        text = squash(self.text)
        self.assertIn("The plugin is instructions only: it runs no code and sends nothing "
                      "anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, "
                      "on your yes, writes your Google products through Google's APIs with your "
                      "Google sign-in.", text)
        for url in ("https://adcopilot.cloud/privacy", "https://adcopilot.cloud/terms",
                    "support@adcopilot.cloud",
                    "https://github.com/AtromxIntelligence/adcopilot-microsoft-ads-plugin/issues"):
            self.assertIn(url, text, url)

    def test_it_lists_every_command_and_skill(self):
        for name in COMMANDS:
            self.assertIn("`/adcopilot-microsoft-ads:%s`" % name, self.text, name)
        for skill in SKILLS:
            self.assertIn("**%s**" % skill, self.text, skill)

    def test_it_has_the_sections_the_ship_script_and_the_reviewer_read(self):
        for heading in ("## Install", "## What you get", "## Data", "## Support",
                        "## Version", "## Licence", "## What CI runs"):
            self.assertIn("\n" + heading + "\n", self.text, heading)


if __name__ == "__main__":
    unittest.main()
