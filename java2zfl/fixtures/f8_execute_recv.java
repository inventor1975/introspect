public class F8 {
  public void run(HttpServletRequest req, java.sql.Statement stmt, java.util.concurrent.Executor pool) throws Exception {
    String v = req.getParameter("v");            // source
    stmt.execute("DELETE FROM t WHERE k=" + v);   // EXPECT: REFUTED [sql] (Statement receiver)
    pool.execute(null);                           // EXPECT: nothing (Executor receiver, not SQL)
  }
}
