public class Web {
  public void handle(HttpServletRequest req, java.sql.Statement stmt, Dao dao) throws Exception {
    String id = req.getParameter("id");
    dao.q(stmt, id);   // EXPECT: REFUTED cross-file (Dao.q param1 -> SQL)
  }
}
