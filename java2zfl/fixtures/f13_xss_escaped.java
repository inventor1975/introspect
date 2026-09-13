import org.apache.commons.text.StringEscapeUtils;
public class F13 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    String q = req.getParameter("q");
    resp.getWriter().write(StringEscapeUtils.escapeHtml4(q));  // clean: escaped for xss
    resp.getWriter().write(q);                                  // EXPECT: REFUTED [xss]
  }
}
