import os
import subprocess

def run_mode():
    if os.environ.get("MODE") in ("fast", "slow"):    # an environment variable: another process may change it
        subprocess.run("run --" + os.environ.get("MODE"), shell=True)   # EXPECT EARNED IF STABLE
