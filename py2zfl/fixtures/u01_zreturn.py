import os, somelib
def h(s):
    return somelib.f(s)
os.system(h(input()))            # EXPECT OPEN (was silent: Z return became F)
