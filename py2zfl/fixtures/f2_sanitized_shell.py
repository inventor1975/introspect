import os, shlex
cmd = shlex.quote(input())   # sanitised
os.system(cmd)               # EXPECT: EARNED [shell]
