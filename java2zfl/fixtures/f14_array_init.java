public class F14 {
  public void run(HttpServletRequest req) throws Exception {
    String cmd = req.getParameter("cmd");
    String[] arr = {"/bin/sh", "-c", cmd};      // bare array initializer (no `new`)
    new ProcessBuilder(arr).start();            // EXPECT: REFUTED [shell]
  }
}
