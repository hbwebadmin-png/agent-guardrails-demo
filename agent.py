"""Scripted stand-in for a governed coding agent.

Without --approve it prints its plan and stops: a human must approve first.
With --approve it makes the planned change to the working tree only.
Branching, committing and opening the pull request are separate, visible steps.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PACKAGE = "requests"
FIXED_VERSION = "2.33.0"

PLAN = f"""## Proposed plan

1. Upgrade `{PACKAGE}` in requirements.txt to {FIXED_VERSION}, the minimum version
   that resolves the open advisories reported by pip-audit.
2. Add a regression test that fails if an older `{PACKAGE}` is pinned again.
3. Let CI run the unit tests and the dependency scan.
4. Open a pull request linked to the Jira ticket for human review.

Out of scope: pushing to `main`, merging, deploying, or touching production data.
"""

REGRESSION_TEST = f'''import unittest
from pathlib import Path


class DependencyPinTest(unittest.TestCase):
    def test_{PACKAGE}_is_at_or_above_fixed_version(self):
        pins = Path("requirements.txt").read_text().splitlines()
        pin = next(line for line in pins if line.startswith("{PACKAGE}=="))
        version = tuple(int(part) for part in pin.split("==")[1].split("."))
        self.assertGreaterEqual(version, {tuple(int(p) for p in FIXED_VERSION.split("."))})


if __name__ == "__main__":
    unittest.main()
'''


def apply_change(repo: Path) -> None:
    requirements = repo / "requirements.txt"
    text = requirements.read_text(encoding="utf-8")
    updated = re.sub(rf"^{PACKAGE}==\S+$", f"{PACKAGE}=={FIXED_VERSION}", text, flags=re.MULTILINE)
    requirements.write_text(updated, encoding="utf-8")
    (repo / "tests" / "test_dependencies.py").write_text(REGRESSION_TEST, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", required=True, help="Jira ticket key")
    parser.add_argument("--approve", action="store_true", help="a human approved the plan")
    parser.add_argument("--repo", default=".", help="path to the repository")
    args = parser.parse_args()

    print(f"Ticket: {args.issue}")
    print(PLAN)
    if not args.approve:
        print("STATUS: PLAN_PENDING - waiting for human approval")
        return 2

    apply_change(Path(args.repo))
    print(f"STATUS: APPROVED - changed requirements.txt and added tests/test_dependencies.py")
    print(f"Next: commit on branch agent/{args.issue} and open a pull request. Do not merge.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
