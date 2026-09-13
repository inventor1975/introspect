import java.util.Set;
public class F4 {
  static final Set<String> ALLOWED = Set.of("ls","pwd","whoami");
  public void run(HttpServletRequest req) throws Exception {
    String cmd = req.getParameter("cmd");        // source: tainted
    if (ALLOWED.contains(cmd)) {                  // whitelist guard -> cmd is validated
      Runtime.getRuntime().exec(cmd);             // EXPECT: nothing (guarded)
    }
  }
}
