import os
def h(p, c):
    if c:
        return p
    p = "safe"
    return p
os.system(h(input(), True))      # EXPECT REFUTED
