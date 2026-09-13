import os
page = input()
if page in ('home','about','contact'):   # whitelist guard -> narrowed
    os.system('render ' + page)           # EXPECT: EARNED (guarded)
os.system('render ' + page)               # EXPECT: REFUTED (outside guard)
