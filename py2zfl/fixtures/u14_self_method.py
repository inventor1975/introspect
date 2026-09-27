import os
class S:
    def clean(self, v):
        return v
    def go(self):
        os.system(self.clean(input()))   # EXPECT REFUTED (self.method passes it)
