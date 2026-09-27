public class F45 {
  static final java.util.regex.Pattern P = java.util.regex.Pattern.compile("^[a-z]+$");
  static final java.util.Map<String, String> COLS = java.util.Map.of("n", "name", "d", "date");
  public void run(HttpServletRequest req, java.sql.Statement st) throws Exception {
    String t = req.getParameter("t");
    if (t == null || !P.matcher(t).matches()) { return; }      // a compound whitelist + early return
    st.executeQuery("SELECT * FROM " + t);                      // clean
    String col = COLS.getOrDefault(req.getParameter("c"), "name");
    st.executeQuery("SELECT " + col + " FROM x");               // clean: a lookup in a literal-only table
    String k = req.getParameter("k");
    st.executeQuery("SELECT * FROM y WHERE k='" + k + "'");     // EXPECT: REFUTED
  } }
