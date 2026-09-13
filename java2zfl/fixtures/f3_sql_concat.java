public class F3 {
  public void run(HttpServletRequest req, java.sql.Statement stmt) throws Exception {
    String id = req.getParameter("id");
    stmt.executeQuery("SELECT * FROM u WHERE id=" + id);   // EXPECT: REFUTED [sql]
  }
}
