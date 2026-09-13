public class F1 {
  public void run(HttpServletRequest req) throws Exception {
    String cmd = req.getParameter("cmd");   // source
    Runtime.getRuntime().exec(cmd);         // EXPECT: REFUTED [shell]
  }
}
