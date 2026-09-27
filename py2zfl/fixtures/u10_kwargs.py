import os
def run(cmd="ls"):
    os.system(cmd)
run(cmd=input())                 # EXPECT REFUTED (keyword argument)
