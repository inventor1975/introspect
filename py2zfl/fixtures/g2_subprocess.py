import subprocess
c = input()
subprocess.run(c)                 # EXPECT: (no sink — shell=False default)
subprocess.run(c, shell=True)     # EXPECT: REFUTED [shell]
