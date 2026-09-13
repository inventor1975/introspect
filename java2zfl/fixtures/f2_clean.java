public class F2 {
  public void run() throws Exception {
    String cmd = "ls -la";                  // constant
    Runtime.getRuntime().exec(cmd);         // EXPECT: (clean, no finding)
  }
}
