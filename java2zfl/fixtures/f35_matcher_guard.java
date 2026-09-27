public class F35 { static final java.util.regex.Pattern P = java.util.regex.Pattern.compile("^[a-z]+$");
  static String filter(String input) { if (!P.matcher(input).matches()) { return null; } return input; }
  public void doPost(HttpServletRequest request) throws Exception {
    String f = filter(request.getParameter("x"));
    Runtime.getRuntime().exec("ls " + f);      // EXPECT: nothing (full-match whitelist before the return)
  } }
