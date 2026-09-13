public class X1 {
  void runCmd(String c) throws Exception { Runtime.getRuntime().exec(c); }
  void handle(HttpServletRequest req) throws Exception {
    String cmd = req.getParameter("cmd");
    runCmd(cmd);          // EXPECT: REFUTED (summary: runCmd param -> shell)
    runCmd("safe");       // EXPECT: (clean)
  }
}
