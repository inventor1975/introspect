import os
cmd = get_it()         # unknown call -> don't know
os.system(cmd)         # EXPECT: OPEN [shell]
