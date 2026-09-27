import os
try:
    cmd = input()
except Exception:
    cmd = "ls"
os.system(cmd)                   # EXPECT REFUTED
