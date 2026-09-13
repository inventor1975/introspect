public class F6 {
  public void run(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    String q = req.getParameter("q");            // source
    resp.getWriter().write(q);                    // EXPECT: REFUTED [xss] (response writer chain)
    java.io.PrintWriter w = resp.getWriter();
    w.write(q);                                   // EXPECT: REFUTED [xss] (typed writer var)
  }
}
