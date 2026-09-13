using System.Data.SqlClient;
public class Dao {
  public void Q(string id) { var c = new SqlCommand("SELECT * FROM u WHERE id=" + id, conn); c.ExecuteReader(); }
}
