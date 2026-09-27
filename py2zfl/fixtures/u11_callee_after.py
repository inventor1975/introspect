import os
def outer(v):
    return inner(v)
def inner(v):
    return v
os.system(outer(input()))        # EXPECT REFUTED (callee defined after the caller)
