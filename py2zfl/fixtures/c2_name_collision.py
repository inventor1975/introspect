import os
class DB:
    def execute(self, q):
        os.system(q)            # THIS execute is dangerous
class Logger:
    def execute(self, msg):
        return len(msg)         # THIS execute is harmless (same name!)
log = Logger()
log.execute(input())            # EXPECT: nothing (Logger.execute is not a sink) — receiver-aware, no bare-name FP
db = DB()
db.execute(input())             # EXPECT: REFUTED (DB.execute IS a sink)
