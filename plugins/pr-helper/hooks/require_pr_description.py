import json
import re
import sys

MARKER = "## Acceptance criteria"


def body_of(command):
    match = re.search(r"--body-file[ =]+(['\"]?)([^'\"\s]+)\1", command)
    if not match:
        return command
    try:
        with open(match.group(2)) as body_file:
            return body_file.read()
    except OSError:
        return ""


def main():
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    if not re.search(r"\bgh\s+pr\s+create\b", command) or MARKER in body_of(command):
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Use the pr-helper:pr-description skill to write this PR's title and body first.",
        }
    }))


main()
