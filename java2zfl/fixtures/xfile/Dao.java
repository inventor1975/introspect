public class Dao {
  public void q(java.sql.Statement stmt, String id) throws Exception {
    stmt.executeQuery("SELECT * FROM u WHERE id=" + id);   // id reaches SQL sink
  }
}
