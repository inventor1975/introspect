import os
def clean(x):
    import shlex; return shlex.quote(x)   # returns neutralised
os.system(clean(input()))   # EXPECT: EARNED (passes through a sanitiser)
def echo(x): return x       # passes taint through
os.system(echo(input()))    # EXPECT: REFUTED (taint passes through)
