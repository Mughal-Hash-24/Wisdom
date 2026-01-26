import sys
import subprocess
import os
import shutil

# 1. Dynamically find 'uv'
UV_PATH = shutil.which("uv")
LOG_FILE = r"D:\WISDOM\WISDOM\90_System\Scripts\mcp_debug.log"


def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except:
        pass


def main():
    if not UV_PATH:
        log("CRITICAL: 'uv' not found.")
        sys.exit(1)

    # 2. THE COMMAND (Updated for Heavy Driver)
    # We removed "server" from the end.
    cmd = [UV_PATH, "tool", "run", "--quiet", "notebooklm-mcp"]

    # 3. Environment Setup (UTF-8 Force)
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONLEGACYWINDOWSSTDIO"] = "0"
    env["NO_COLOR"] = "1"

    try:
        # Start the Tool
        process = subprocess.Popen(
            cmd,
            stdin=sys.stdin,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            encoding='utf-8',
            errors='replace',
            env=env
        )

        # Filter Loop
        while True:
            line = process.stdout.readline()
            if not line:
                break

            # Pass valid JSON, filter the rest
            if line.strip().startswith('{'):
                sys.stdout.write(line)
                sys.stdout.flush()
            else:
                log(f"Filtered: {line.strip()[:20]}...")

    except Exception as e:
        log(f"CRITICAL ERROR: {str(e)}")


if __name__ == "__main__":
    main()