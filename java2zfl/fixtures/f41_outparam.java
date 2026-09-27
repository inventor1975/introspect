public class F41 {
  static void addOwner(StringBuilder sql, String owner) { sql.append(" AND owner = '").append(owner).append("'"); }
  public void run(HttpServletRequest req, java.sql.Statement st) throws Exception {
    StringBuilder sql = new StringBuilder("SELECT * FROM p WHERE 1=1");
    addOwner(sql, req.getParameter("owner"));   // the helper stores the value into the CALLER's builder
    st.executeQuery(sql.toString());            // EXPECT: REFUTED (was EARNED)
  } }
