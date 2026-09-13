from dao import run_query
def view():
    cmd = input()        # source in file A
    run_query(cmd)       # EXPECT: REFUTED — cross-file (view -> dao.run_query -> sink)
