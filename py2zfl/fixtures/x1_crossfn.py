import os
def run_cmd(c):
    os.system(c)          # c reaches a shell sink
run_cmd(input())          # EXPECT: REFUTED (tainted arg -> summary -> sink)
run_cmd("ls")             # EXPECT: EARNED (constant)
