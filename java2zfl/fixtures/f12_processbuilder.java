public class F12 {
  public void run(HttpServletRequest req) throws Exception {
    String fp = req.getParameter("fp");                      // source
    String[] cmd = new String[]{"sh","-c","ls " + fp};        // array taint
    ProcessBuilder pb = new ProcessBuilder(cmd);              // EXPECT: REFUTED [shell] (ctor sink via array)
    pb.start();
  }
}
