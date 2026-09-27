public class F55 {
  static final java.util.Set<String> CAMPAIGNS = java.util.Set.of("SPRING", "SUMMER");
  public void run(HttpServletRequest req, java.sql.Statement st) throws Exception {
    String code = java.util.Optional.ofNullable(req.getParameter("c"))
        .map(String::trim).map(c -> CAMPAIGNS.contains(c) ? c : "DEFAULT").orElse("DEFAULT");
    st.executeQuery("SELECT * FROM p WHERE code='" + code + "'");   // clean: a whitelist inside the lambda
    String raw = java.util.Optional.ofNullable(req.getParameter("r")).map(String::trim).orElse("");
    st.executeQuery("SELECT * FROM p WHERE code='" + raw + "'");    // EXPECT: REFUTED (was OPEN: ofNullable unknown)
  } }
