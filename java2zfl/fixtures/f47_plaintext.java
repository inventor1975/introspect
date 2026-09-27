public class F47 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    resp.setContentType("text/plain;charset=UTF-8");
    resp.setHeader("X-Content-Type-Options", "nosniff");
    resp.getWriter().println("status for " + req.getParameter("id"));   // clean: not HTML
  } }
