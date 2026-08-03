"""Deterministic intake for every skill in skills/ — the write side of the loop.

Two modes, one script:

  --check   Read-only. Refuse secrets, report a missing or stale nudge.
            Runs on pull requests, including from forks.
  (default) Repair in place: install the nudge, sync index.md, commit.
            Runs on push to main, where write access always exists.

The split exists because this repo is org-visible, so most contributions
arrive from forks whose branches GITHUB_TOKEN cannot write to. Installing
after merge works identically for forks and direct branches.

The nudge is installed rather than merely demanded, so a contributor who has
never heard of it still ships a skill that carries it. That is what makes the
improvement loop self-sustaining instead of dependent on anyone remembering a
convention.

Injection is idempotent by construction — a match-and-replace on the marker,
never a blind append. Absent, present-and-current, present-but-stale, and
present-twice all converge on exactly one current copy.

Exits non-zero on a secret finding, in either mode. Judgement (overlap,
genericity, completeness, security, merge-vs-reference routing) belongs to the
reviewer agent, not here.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

SKILLS = Path("skills")
NUDGE_SOURCE = Path("nudge.md")
INDEX = Path("index.md")

MARKER = "ogp-improvement-nudge"

# Coarse net for the mistakes that actually happen — a pasted token or webhook.
# GitHub's own push protection is the real backstop; this fails the PR early so
# a reviewer never spends time on a diff that has to be rewritten anyway.
SECRET_PATTERNS = [
    (r"gh[pousr]_[A-Za-z0-9]{16,}", "GitHub token"),
    (r"github_pat_[A-Za-z0-9_]{20,}", "GitHub fine-grained token"),
    (r"sk-ant-[A-Za-z0-9_-]{16,}", "Anthropic API key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
    (r"AIza[0-9A-Za-z_-]{35}", "Google API key"),
    (r"https://hooks\.(zapier|slack)\.com/\S+", "webhook URL"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "private key"),
    (r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"\s]{16,}['\"]",
     "hardcoded credential"),
]


def canonical_nudge() -> str:
    """Pull the installable block out of the first fenced section of nudge.md."""
    text = NUDGE_SOURCE.read_text(encoding="utf-8")
    match = re.search(r"```markdown\n(.*?)\n```", text, re.DOTALL)
    if not match:
        sys.exit(f"{NUDGE_SOURCE}: no ```markdown fence holding the nudge block")
    return match.group(1).strip()


def frontmatter(text: str) -> dict[str, str]:
    """Read YAML frontmatter without a YAML dependency.

    Only flat `key: value` pairs matter here (name, description), so a line
    parser is enough and keeps this stdlib-only per the repo's stack rule.
    """
    match = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip("'\"")
    return fields


def scan_secrets() -> list[str]:
    findings = []
    for path in sorted(SKILLS.rglob("*")):
        if not path.is_file():
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, content):
                findings.append(f"{path}: looks like a {label}")
    return findings


def strip_nudges(text: str) -> str:
    """Remove every installed copy, current or stale, one or many.

    The heading above the marker goes too, since the canonical block carries
    its own.
    """
    return re.sub(
        r"\n*(?:^#{1,6} [^\n]*\n+)?<!-- " + MARKER + r".*?(?=\n#{1,6} |\Z)",
        "\n",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )


def with_nudge(text: str, block: str) -> str:
    return strip_nudges(text).rstrip() + "\n\n" + block + "\n"


def install_nudge(skill_md: Path, block: str) -> bool:
    """Ensure exactly one current copy sits at the end. Idempotent."""
    text = skill_md.read_text(encoding="utf-8")
    updated = with_nudge(text, block)
    if updated == text:
        return False
    skill_md.write_text(updated, encoding="utf-8")
    return True


def purpose_of(fields: dict[str, str]) -> str:
    """One index-table cell: the description's first sentence, trimmed."""
    description = fields.get("description", "").strip()
    if not description:
        return "_no description_"
    first = re.split(r"(?<=[.!?])\s", description)[0].strip()
    return first if len(first) <= 160 else first[:157].rstrip() + "..."


def rebuild_index(author: str) -> bool:
    """Regenerate the Skills table from disk, preserving known owners.

    Owner cannot be derived from a skill's contents, so an existing row keeps
    its owner and a new row gets whoever authored the merge. Editing the table
    by hand still works — the next run reads whatever owner it finds.
    """
    text = INDEX.read_text(encoding="utf-8")
    match = re.search(
        r"(## Skills\n\n\| Name \| Purpose \| Owner \| Status \|\n\|---\|---\|---\|---\|\n)(.*?)(\n\n|\Z)",
        text,
        re.DOTALL,
    )
    if not match:
        print("index.md: no Skills table in the expected shape — skipping")
        return False

    header, body, tail = match.groups()

    owners, statuses = {}, {}
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4:
            name = re.sub(r"\[([^\]]+)\].*", r"\1", cells[0])
            owners[name] = cells[2]
            statuses[name] = cells[3]

    rows = []
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        name = skill_md.parent.name
        fields = frontmatter(skill_md.read_text(encoding="utf-8"))
        owner = owners.get(name) or author or "_unassigned_"
        status = statuses.get(name, "Active")
        rows.append(
            f"| [{name}](skills/{name}/) | {purpose_of(fields)} | {owner} | {status} |"
        )

    if not rows:
        return False

    rebuilt = header + "\n".join(rows) + tail
    updated = text[: match.start()] + rebuilt + text[match.end():]
    if updated == text:
        return False
    INDEX.write_text(updated, encoding="utf-8")
    return True


def commit(paths: list[Path]) -> None:
    """Commit only when content actually changed, so the push can't loop."""
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(
        ["git", "config", "user.email",
         "41898282+github-actions[bot]@users.noreply.github.com"],
        check=True,
    )
    subprocess.run(["git", "add", "--", *map(str, paths)], check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing staged — no commit")
        return
    subprocess.run(
        ["git", "commit", "-m", "Skills intake: install nudge, sync index"], check=True
    )
    subprocess.run(["git", "push"], check=True)


def main() -> None:
    if not SKILLS.is_dir():
        sys.exit("skills/ not found — run from the repo root")

    check_only = "--check" in sys.argv

    findings = scan_secrets()
    if findings:
        print("SECRETS FOUND — refusing this change:")
        for finding in findings:
            print(f"  {finding}")
        print("\nRotate anything real that was exposed, then remove it from the diff.")
        sys.exit(1)

    block = canonical_nudge()
    skills = sorted(SKILLS.glob("*/SKILL.md"))

    if check_only:
        stale = [
            str(s) for s in skills
            if s.read_text(encoding="utf-8") != with_nudge(s.read_text(encoding="utf-8"), block)
        ]
        if stale:
            print("Nudge missing or out of date in:")
            for path in stale:
                print(f"  {path}")
            print("\nNothing for you to do — it is installed automatically on merge.")
        else:
            print("All skills carry the current nudge.")
        print(f"\nChecked {len(skills)} skill(s), no secrets found.")
        return

    changed: list[Path] = []
    for skill_md in skills:
        if install_nudge(skill_md, block):
            print(f"nudge installed or refreshed: {skill_md}")
            changed.append(skill_md)

    if rebuild_index(os.environ.get("MERGE_AUTHOR", "")):
        print("index.md: Skills table synced with disk")
        changed.append(INDEX)

    if not changed:
        print("nothing to do — every skill carries the current nudge, index matches disk")
        return

    if os.environ.get("GITHUB_ACTIONS"):
        commit(changed)


if __name__ == "__main__":
    main()
