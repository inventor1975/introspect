import org.apache.commons.lang3.StringUtils;
public class F53 {
  static final java.util.regex.Pattern W = java.util.regex.Pattern.compile("^[a-z]+$");
  private boolean isPlainWord(String s) { return W.matcher(s).matches(); }
  public void run(HttpServletRequest req, java.sql.Statement st) throws Exception {
    String a = req.getParameter("a");
    if (!StringUtils.isNumeric(a)) { return; }
    st.executeQuery("SELECT * FROM t WHERE id=" + a);          // clean
    String b = req.getParameter("b");
    if (!isPlainWord(b)) { return; }                           // the program's own validator
    st.executeQuery("SELECT * FROM t WHERE tag='" + b + "'");  // clean
    String c = req.getParameter("c");
    try { Long.parseLong(c); } catch (NumberFormatException e) { return; }
    st.executeQuery("SELECT * FROM t WHERE n=" + c);           // clean: parsed or returned
    String d = req.getParameter("d");
    if (!(d.equalsIgnoreCase("asc") || d.equalsIgnoreCase("desc"))) { d = "asc"; }
    st.executeQuery("SELECT * FROM t ORDER BY x " + d);        // clean
    String e = req.getParameter("e");
    st.executeQuery("SELECT * FROM t WHERE k='" + e + "'");    // EXPECT: REFUTED
  } }
