public class F46 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    String q = req.getParameter("q");
    resp.getWriter().println("<a href=\"/s?q=" + java.net.URLEncoder.encode(q, "UTF-8") + "\">s</a>");  // clean
    resp.getWriter().println("<p>" + q.replaceAll("[^A-Za-z0-9 .,-]", "") + "</p>");                      // clean
    resp.getWriter().println("<p>" + q.replaceAll("[<>]", "") + "</p>");                                  // EXPECT: REFUTED (not a whitelist)
  } }
