import os
parts = ["ls"]
parts.append(input())
os.system(" ".join(parts))       # EXPECT REFUTED
