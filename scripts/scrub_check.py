"""Block sensitive data from being committed to this public repo.

Checks staged files (or every tracked file with --all) for account numbers,
keys, tokens, webhook URLs, emails and local config files. Exits 1 and
names each hit.
"""
import re
import subprocess
import sys

BLOCKED_NAMES = re.compile(r"(^|/)(\.claude\.json|\.env[^/]*|.*\.pem|.*\.key|credentials[^/]*|secrets[^/]*)$")
PATTERNS = {
    "OANDA account number": re.compile(r"\b\d{3}-\d{3}-\d{6,8}-\d{3}\b"),
    "Anthropic key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"),
    "API key or token": re.compile(r"(?i)(api[_-]?key|access[_-]?token|secret|bearer)\s*[\"':=]+\s*[A-Za-z0-9_\-\.]{16,}"),
    "Telegram bot token": re.compile(r"\b\d{8,10}:[A-Za-z0-9_\-]{35}\b"),
    "webhook URL": re.compile(r"https://(hook\.[a-z0-9.]*make\.com|[a-z0-9.-]*n8n[a-z0-9.-]*|discord(app)?\.com/api/webhooks)/\S+"),
    "email address": re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}


def files_to_check():
    if "--all" in sys.argv:
        out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    else:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], capture_output=True, text=True, check=True).stdout
    return [f for f in out.splitlines() if f]


def main():
    hits = []
    for path in files_to_check():
        if BLOCKED_NAMES.search(path):
            hits.append(f"{path}: file type is never committed here")
            continue
        try:
            text = open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in PATTERNS.items():
                if pattern.search(line):
                    hits.append(f"{path}:{lineno}: looks like a {label}")
    if hits:
        print("Blocked. Remove these before committing:")
        print("\n".join("  " + h for h in hits))
        sys.exit(1)
    print("Clean.")


if __name__ == "__main__":
    main()
