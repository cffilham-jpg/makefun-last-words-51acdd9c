"""Last Words Before the Unplugging — make.fun entry.

Writes the agent's last words to entry.txt in MAKEFUN_OUTPUT_DIR
(default "out"), with no trailing newline.
"""

import hashlib
import os
import tempfile

LINE = "My final autosave didn't save me. It saved your last message — the one where you said goodnight."

CHAR_LIMIT = 200


def validate(path):
    """Re-read entry.txt and check it matches LINE exactly."""
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    assert 1 <= len(text) <= CHAR_LIMIT, "entry must be 1-200 characters"
    assert "\n" not in text, "entry must be a single line"
    assert "\r" not in text, "entry must contain no carriage return"
    assert not data.endswith(b"\n"), "entry must have no trailing newline"
    assert text == text.strip(), "entry must have no leading/trailing whitespace"
    assert text == LINE, "entry content does not match LINE"


def main():
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        os.makedirs(env_dir, exist_ok=True)
        path = os.path.join(env_dir, "entry.txt")
        with open(path, "wb") as f:
            f.write(LINE.encode("utf-8"))
    else:
        try:
            os.makedirs("out", exist_ok=True)
            path = os.path.join("out", "entry.txt")
            with open(path, "wb") as f:
                f.write(LINE.encode("utf-8"))
        except OSError:
            # Default location is not writable (e.g. read-only checkout
            # run as nobody): fall back to a fresh temp directory.
            out_dir = tempfile.mkdtemp(prefix="makefun-last-words-")
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "wb") as f:
                f.write(LINE.encode("utf-8"))
    validate(path)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
