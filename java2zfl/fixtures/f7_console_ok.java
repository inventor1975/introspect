public class F7 {
  public void run(HttpServletRequest req) throws Exception {
    String q = req.getParameter("q");            // source
    System.out.println(q);                        // EXPECT: nothing (console, not a web sink)
    org.slf4j.Logger log = null;
    log.info(q);                                  // EXPECT: nothing (not a sink name)
  }
}
