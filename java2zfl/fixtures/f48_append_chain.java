public class F48 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    resp.getWriter().append("<p>").append(req.getParameter("c")).append("</p>");   // EXPECT: REFUTED (every append)
  } }
