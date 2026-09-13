import java.util.Set;
public class F5 {
  static final Set<String> ALLOWED = Set.of("ls","pwd","whoami");
  public void run(HttpServletRequest req) throws Exception {
    String cmd = req.getParameter("cmd");        // source: tainted
    if (!ALLOWED.contains(cmd)) { return; }       // negated guard + early return
    Runtime.getRuntime().exec(cmd);               // EXPECT: nothing (validated above)
  }
}
