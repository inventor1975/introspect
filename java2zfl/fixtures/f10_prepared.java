public class F10 {
  public void run(HttpServletRequest req, java.sql.Connection conn) throws Exception {
    String id = req.getParameter("id");                             // source
    java.sql.PreparedStatement ok = conn.prepareStatement("SELECT * FROM u WHERE id=?");
    ok.setString(1, id);
    ok.executeQuery();                                              // EXPECT: nothing (parameterised)
    conn.prepareStatement("SELECT * FROM u WHERE id=" + id);        // EXPECT: REFUTED [sql] (concatenated)
  }
}
