"""The manifest, the marketplace file and the connector registration.

Everything here is read from files in this repository, with the standard
library only, and no test reads an environment variable. Run with

    python3 -m unittest discover -s tests -v

from the repository root.

What each check protects:

* the plugin name is permanent once the directory lists it, and the display
  name is the one the founder decided on, so both are pinned;
* the directory's pre-submission checklist asks for a name made of lowercase
  letters, digits and hyphens, a description, a version, an author, a
  homepage, a licence, keywords and an icon, so each is held to its value;
* `.mcp.json` names the same server key and address as every other AdCopilot
  plugin, the Google Ads one included, so that Claude sees one AdCopilot
  connector however many of them are added; in the plugins first released on
  2026-10-23 it is also the same file, byte for byte;
* the marketplace entry carries no listing fields, which the validator reports
  as unknown there.
"""

import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPO = "adcopilot-microsoft-ads-plugin"
NAME = "adcopilot-microsoft-ads"
DISPLAY_NAME = "AdCopilot for Microsoft Ads (Bing Ads)"
OWNER_NAME = "Atromx Intelligence"

# The one connector file, identical in the AdCopilot plugin repositories first
# released on 2026-10-23: one line, ending with a newline.
CANONICAL_MCP_TEXT = (
    '{"mcpServers":{"adcopilot":{"type":"http","url":"https://mcp.adcopilot.cloud/mcp"}}}\n'
)
CANONICAL_MCP = {
    "mcpServers": {
        "adcopilot": {"type": "http", "url": "https://mcp.adcopilot.cloud/mcp"}
    }
}

# The AdCopilot mark, copied from the Claude plugin for Google Ads. It is
# AdCopilot's own: never a Microsoft, Bing or Google logo.
ICON_SHA256 = "48b8db13867010ea323fb42c557a69a09053bc7aaf7bce129e8a5541935a28d6"

EXPECTED_KEYS = [
    "name", "version", "description", "author", "homepage", "privacyPolicyUrl",
    "documentationUrl", "termsOfServiceUrl", "supportUrl", "repository",
    "license", "keywords", "displayName", "icon",
]

NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
KEYWORD_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


class Manifest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manifest = load(".claude-plugin/plugin.json")

    def test_the_field_set_is_exactly_the_decided_one_in_order(self):
        self.assertEqual(list(self.manifest.keys()), EXPECTED_KEYS)

    def test_name_display_name_and_author(self):
        m = self.manifest
        self.assertEqual(m["name"], NAME)
        self.assertRegex(m["name"], NAME_RE)
        self.assertEqual(m["displayName"], DISPLAY_NAME)
        self.assertEqual(m["author"], {"name": OWNER_NAME, "url": "https://adcopilot.cloud"})
        self.assertEqual(m["license"], "MIT")

    def test_version_is_semver(self):
        self.assertRegex(self.manifest["version"], SEMVER_RE)
        self.assertEqual(self.manifest["version"], "0.1.0")

    def test_urls_are_https_and_the_decided_ones(self):
        m = self.manifest
        self.assertEqual(m["homepage"], "https://adcopilot.cloud")
        self.assertEqual(m["privacyPolicyUrl"], "https://adcopilot.cloud/privacy")
        self.assertEqual(m["documentationUrl"], "https://adcopilot.cloud/docs/")
        self.assertEqual(m["termsOfServiceUrl"], "https://adcopilot.cloud/terms")
        self.assertEqual(m["supportUrl"], "https://github.com/AtromxIntelligence/%s/issues" % REPO)
        self.assertEqual(m["repository"], "https://github.com/AtromxIntelligence/%s" % REPO)
        urls = [m["homepage"], m["privacyPolicyUrl"], m["documentationUrl"],
                m["termsOfServiceUrl"], m["supportUrl"], m["repository"], m["author"]["url"]]
        for url in urls:
            self.assertTrue(url.startswith("https://"), url)

    def test_keywords_are_few_lowercase_kebab_case_and_unique(self):
        keywords = self.manifest["keywords"]
        self.assertLessEqual(len(keywords), 15)
        self.assertEqual(len(keywords), len(set(keywords)))
        for word in keywords:
            self.assertRegex(word, KEYWORD_RE)
        # The words people type for this product are in there.
        for word in ("microsoft-ads", "bing-ads", "uet-tag"):
            self.assertIn(word, keywords)

    def test_description_leads_with_the_product_and_ends_with_the_owner_line(self):
        d = self.manifest["description"]
        self.assertTrue(d.startswith("Microsoft Ads (Bing Ads)"), d[:40])
        self.assertTrue(d.endswith("Made by Atromx Intelligence, not by Microsoft."), d[-60:])
        self.assertLessEqual(len(d), 700, "the listing text grew to %d characters" % len(d))
        # The today and later halves, said plainly in the listing too.
        self.assertIn("comes when Microsoft approves AdCopilot's API access", d)
        self.assertIn("there is no date yet", d)
        self.assertIn("proposed first and made only on your yes", d)

    def test_the_icon_is_our_own_png(self):
        icon = ROOT / self.manifest["icon"][2:]  # without the leading "./"
        self.assertEqual(self.manifest["icon"], "./.claude-plugin/icon.png")
        data = icon.read_bytes()
        self.assertTrue(data.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(hashlib.sha256(data).hexdigest(), ICON_SHA256,
                         "the icon must be AdCopilot's own mark, not another company's")
        self.assertFalse((ROOT / ".claude-plugin" / "icon.svg").exists())

    def test_readme_version_paragraph_matches_the_manifest(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        found = re.findall(r"^\*\*(\d+\.\d+\.\d+) \((\d{4}-\d{2}-\d{2})[^)]*\)\*\*", text, re.M)
        self.assertEqual(len(found), 1, "one bold version paragraph, which the ship script reads")
        self.assertEqual(found[0][0], self.manifest["version"])
        self.assertIn("**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)**", text)


class ConnectorRegistration(unittest.TestCase):

    def test_mcp_json_is_the_canonical_file_byte_for_byte(self):
        raw = (ROOT / ".mcp.json").read_text(encoding="utf-8")
        self.assertEqual(raw, CANONICAL_MCP_TEXT)
        self.assertEqual(json.loads(raw), CANONICAL_MCP)

    def test_the_server_key_and_address_are_the_shared_ones(self):
        servers = load(".mcp.json")["mcpServers"]
        self.assertEqual(list(servers), ["adcopilot"])
        server = servers["adcopilot"]
        self.assertEqual(server, {"type": "http", "url": "https://mcp.adcopilot.cloud/mcp"})
        # Same spelling as the live plugin: lowercase, no trailing slash, no query.
        self.assertNotIn("?", server["url"])
        self.assertFalse(server["url"].endswith("/"))
        self.assertEqual(server["url"], server["url"].lower())


class Marketplace(unittest.TestCase):

    def test_the_marketplace_names_the_plugin_and_carries_no_listing_fields(self):
        market = load(".claude-plugin/marketplace.json")
        self.assertEqual(market["name"], REPO)
        self.assertEqual(market["owner"], {"name": OWNER_NAME, "url": "https://adcopilot.cloud"})
        self.assertTrue(market["description"].strip())
        self.assertEqual(len(market["plugins"]), 1)
        entry = market["plugins"][0]
        self.assertEqual(entry["name"], NAME)
        self.assertEqual(entry["source"], "./")
        self.assertEqual(entry["category"], "Marketing")
        self.assertTrue(entry["description"].strip())
        # The directory's listing fields belong in plugin.json: the validator
        # reports them as unknown inside a marketplace entry.
        self.assertEqual(sorted(entry), ["category", "description", "name", "source"])
        self.assertEqual(sorted(market), ["description", "name", "owner", "plugins"])


if __name__ == "__main__":
    unittest.main()
