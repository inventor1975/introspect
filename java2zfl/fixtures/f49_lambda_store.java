public class F49 {
  public void run(HttpServletRequest req, java.sql.Statement st, java.util.Map<String, String> m) throws Exception {
    StringBuilder sb = new StringBuilder("SELECT * FROM t WHERE 1=1");
    m.forEach((k, v) -> sb.append(" AND ").append(k).append("='").append(v).append("'"));
    st.executeQuery(sb.toString());   // EXPECT: OPEN (the lambda's parameters are unknown; the store is kept)
  } }
