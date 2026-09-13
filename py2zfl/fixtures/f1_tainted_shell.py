import os
cmd = input()          # source -> tainted
os.system(cmd)         # EXPECT: REFUTED [shell]
