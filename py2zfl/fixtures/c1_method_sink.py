import os
class Runner:
    def go(self, cmd):
        os.system(cmd)          # method reaches a shell sink
r = Runner()
r.go(input())                   # EXPECT: REFUTED (Runner.go -> sink)
r.go("ls")                      # EXPECT: EARNED (constant)
