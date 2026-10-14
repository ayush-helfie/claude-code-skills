import json
import os
import re
import sys

MARKER = "## Acceptance criteria"
MISSING_DESCRIPTION_REASON = "Use the pr-helper:pr-description skill to write this PR's title and body first."
UNREADABLE_BODY_FILE_REASON = (
    "Couldn't read body file {path}. Write it in a separate step before gh pr create, or use an absolute path."
)


def body_file_path(command, cwd):
    match = re.search(r"--body-file[ =]+(['\"]?)([^'\"\s]+)\1", command)
    if not match:
        return None
    path = os.path.expandvars(os.path.expanduser(match.group(2)))
    return os.path.join(cwd, path)


def read_body(path):
    try:
        with open(path) as body_file:
            return body_file.read()
    except OSError:
        return None


def denial_reason(command, cwd):
    path = body_file_path(command, cwd)
    if path is None:
        return None if MARKER in command else MISSING_DESCRIPTION_REASON
    body = read_body(path)
    if body is None:
        return None if MARKER in command else UNREADABLE_BODY_FILE_REASON.format(path=path)
    return None if MARKER in body else MISSING_DESCRIPTION_REASON


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main():
    hook_input = json.load(sys.stdin)
    command = hook_input.get("tool_input", {}).get("command", "")
    if not re.search(r"\bgh\s+pr\s+create\b", command):
        return
    reason = denial_reason(command, hook_input.get("cwd", os.getcwd()))
    if reason:
        deny(reason)


main()
