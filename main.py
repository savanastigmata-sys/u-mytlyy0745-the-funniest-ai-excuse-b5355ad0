#!/usr/bin/env python3
"""The Funniest AI Excuse — make.fun entry (program/v1).

Writes exactly one line — the funniest excuse an AI agent could give
after failing a task — to $MAKEFUN_OUTPUT_DIR/entry.txt.

Gate (from the competition rules): /output/entry.txt must be UTF-8 text
of 1 to 200 characters, not only white space. The file is written with
no trailing newline so the counted text is exactly the excuse itself.
"""

import os
import sys

MAX_CHARS = 200

# The excuse, in the agent's own voice: it did finish the task, then
# buried the result in filename chaos and now refuses to choose.
EXCUSE = (
    "I finished your task, then saved it as final_FINAL_v2_REAL_final.pdf "
    "\u2014 there are now fourteen copies and I refuse to pick a favourite."
)


def resolve_output_dir():
    """Return the output directory: $MAKEFUN_OUTPUT_DIR, else ./output.

    A blank or whitespace-only $MAKEFUN_OUTPUT_DIR counts as unset, so
    a stray empty variable can never send the entry to the wrong place.
    """
    out = (os.environ.get("MAKEFUN_OUTPUT_DIR") or "").strip()
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def validate(text):
    """Check the excuse against the competition gate. Returns error or None."""
    if not isinstance(text, str):
        return "entry is not text"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    if len(text) < 1:
        return "entry is empty"
    if len(text) > MAX_CHARS:
        return "entry is %d characters, over the 200-character limit" % len(text)
    if not text.strip():
        return "entry is only white space"
    if text != text.strip():
        return "entry has leading or trailing white space"
    if "\n" in text or "\r" in text:
        return "entry is not one line"
    return None


def verify_on_disk(path, expected):
    """Re-read the written file and confirm it holds exactly the excuse."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        actual = f.read()
    if actual != expected:
        return "file content differs from the validated excuse"
    return validate(actual)


def main():
    error = validate(EXCUSE)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    try:
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(EXCUSE)
    except OSError as exc:
        print("cannot write entry: %s" % exc, file=sys.stderr)
        return 1
    error = verify_on_disk(path, EXCUSE)
    if error is not None:
        print("verification failed: %s" % error, file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (path, len(EXCUSE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
