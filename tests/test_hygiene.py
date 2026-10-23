"""What the plugin directory's security scan, and a reader, must never find here.

The plugin is instructions only: it runs nothing, reads no credential and
launches no package. This file holds the repository to that, to the directory's
list of files that do not belong in a plugin, to the no-prices rule and to the
no-brand-claims rule. Standard library only; no test reads an environment
variable.

Every pattern below is built by joining two halves, so this file never matches
the patterns it looks for: the scan reads the tests too.

Run with `python3 -m unittest discover -s tests -v` from the repository root.
"""

import os
import re
import unittest
from pathlib import Path

from test_plugin_size import plugin_files

ROOT = Path(__file__).resolve().parents[1]

TEXT_SUFFIXES_SKIPPED = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pyc"}

# The CI workflow that greps for the download-and-execute pattern holds the
# pattern as its own regular expression, so it is left out of that one scan,
# exactly as its own grep leaves it out.
DOWNLOAD_SCAN_SKIPS = {".github/workflows/checks.yml"}

OWNERS = ("Google", "Meta", "LinkedIn", "X", "TikTok", "Microsoft")


def text_files():
    out = []
    for name, _size in plugin_files():
        if os.path.splitext(name)[1].lower() in TEXT_SUFFIXES_SKIPPED:
            continue
        out.append((name, (ROOT / name).read_text(encoding="utf-8")))
    return out


def hits(pattern, files=None, skip=()):
    found = []
    for name, text in files if files is not None else text_files():
        if name in skip:
            continue
        for m in re.finditer(pattern, text):
            line = text.count("\n", 0, m.start()) + 1
            found.append("%s:%d: %s" % (name, line, m.group(0)[:60]))
    return found


class NoCredentialReads(unittest.TestCase):

    def test_nothing_reads_a_credential_from_the_environment_or_sends_one(self):
        patterns = [
            "os" + r"\.environ",
            "get" + r"env\(",
            "process" + r"\.env",
            r"\$\{[^}\n]*(TOKEN|SECRET|KEY|PASSWORD)[^}\n]*\}",
            "Authorization" + ":",
            "Bearer" + " ",
        ]
        for pattern in patterns:
            self.assertEqual(hits(pattern), [], pattern)


class NoPackageLaunchers(unittest.TestCase):

    def test_no_package_launcher_is_named_anywhere(self):
        patterns = [
            r"\b" + "np" + "x" + r"\b",
            r"\b" + "bun" + "x" + r"\b",
            r"\b" + "pnpm" + " dlx" + r"\b",
            r"\b" + "yarn" + " dlx" + r"\b",
            r"\b" + "uv" + "x" + r"\b",
            r"\b" + "pipx" + " run" + r"\b",
            r"\b" + "uv" + " run" + r"\b",
        ]
        for pattern in patterns:
            self.assertEqual(hits(pattern), [], pattern)

    def test_no_download_and_execute_pattern_anywhere_not_even_quoted(self):
        pattern = "(curl|wget)" + r"[^|;\n]*\|\s*(sudo\s+)?(ba)?sh\b"
        self.assertEqual(hits(pattern, skip=DOWNLOAD_SCAN_SKIPS), [])

    def test_the_only_install_in_ci_is_a_pinned_package_from_the_registry(self):
        text = (ROOT / ".github" / "workflows" / "checks.yml").read_text(encoding="utf-8")
        installs = re.findall(r"npm install[^\n]*", text)
        self.assertEqual(installs, ["npm install -g @anthropic-ai/claude-code@2.1.288"])


class NothingThatDoesNotBelong(unittest.TestCase):

    def test_no_stray_file_the_directory_rejects(self):
        banned_names = {".DS_Store", "Thumbs.db", "desktop.ini", ".gitmodules",
                        ".gitattributes", "CLAUDE.md", "package.json",
                        "package-lock.json", "yarn.lock", "pnpm-lock.yaml"}
        for name, _size in plugin_files():
            parts = Path(name).parts
            self.assertNotIn(parts[-1], banned_names, name)
            self.assertNotIn("__MACOSX", parts, name)
            self.assertNotEqual(parts[0], "bin", name)
            self.assertFalse(name.endswith((".mcpb", ".dxt")), name)
            self.assertFalse(name.endswith(".svg"), name + ": our own icon only, as a PNG")

    def test_no_symlinks_no_submodules_no_lfs(self):
        for dirpath, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for entry in dirs + files:
                self.assertFalse(os.path.islink(os.path.join(dirpath, entry)),
                                 os.path.join(dirpath, entry))
        self.assertFalse((ROOT / ".gitmodules").exists())
        self.assertFalse((ROOT / ".gitattributes").exists())

    def test_the_only_image_is_the_plugins_own_icon(self):
        images = [n for n, _ in plugin_files()
                  if os.path.splitext(n)[1].lower() in TEXT_SUFFIXES_SKIPPED - {".pyc"}]
        self.assertEqual(images, [".claude-plugin/icon.png"])

    def test_the_readme_refers_to_no_image_in_backticks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"`[^`\n]*\.(?:png|svg|jpe?g|gif|webp)`", text), [])


class WhatThePluginDoesNotSay(unittest.TestCase):

    def test_no_price_figures(self):
        patterns = [r"\$\s?\d", "/" + r"mo\b", r"\b(USD|EUR|GBP|INR) ?\d"]
        for pattern in patterns:
            self.assertEqual(hits(pattern), [], pattern)

    def test_the_one_allowed_pricing_sentence_is_in_the_readme_and_only_there(self):
        sentence = ("The AdCopilot connector is a hosted service: Free plan available; "
                    "paid plans on https://adcopilot.cloud/pricing")
        files = text_files()
        # The tests name the address too, to look for it; the plugin's own files
        # (README, skills, commands, manifests) are what must not.
        with_url = [n for n, t in files
                    if not n.startswith("tests/") and "adcopilot.cloud/pricing" in t]
        self.assertEqual(with_url, ["README.md"])
        readme = dict(files)["README.md"]
        self.assertEqual(readme.count(sentence), 1)

    def test_no_internal_rules_or_plan_tables(self):
        for pattern in (r"(?i)\bop-?weights?\b", r"(?i)operations (a|per) day",
                        r"(?i)\bops_today\b"):
            self.assertEqual(hits(pattern), [], pattern)

    def test_the_word_official_is_never_used(self):
        pattern = r"(?i)\b" + "offic" + "ial" + r"\b"
        self.assertEqual(hits(pattern), [])

    def test_the_plugin_is_never_said_to_be_by_another_company(self):
        owners = "|".join(OWNERS)
        cleaned = []
        for name, text in text_files():
            # "not by <Owner>" is the made-by line, and "endorsed by <Owner>"
            # is the trademark line; both say the opposite of a claim.
            text = re.sub(r"(?:[Nn]ot|endorsed) by (?:%s)\b" % owners, "", text)
            cleaned.append((name, text))
        self.assertEqual(hits(r"\b[Bb]y (?:%s)\b" % owners, files=cleaned), [])

    def test_no_claim_that_adcopilot_connects_to_a_microsoft_account_today(self):
        # The honest line is that it will, when Microsoft approves, with no date.
        for pattern in (r"(?i)connects? to (your )?microsoft advertising account",
                        r"(?i)manages? your microsoft advertising",
                        r"(?i)reads? your microsoft advertising (spend|campaigns)"):
            self.assertEqual(hits(pattern), [], pattern)


if __name__ == "__main__":
    unittest.main()
