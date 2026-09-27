import org.apache.commons.text.StringEscapeUtils;
public class F51 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    String t = (String) req.getAttribute("tenant");            // set by someone else: unknown, not clean
    resp.getWriter().print("<p>" + t + "</p>");                // EXPECT: OPEN
    String e = StringEscapeUtils.unescapeHtml4(StringEscapeUtils.escapeHtml4(req.getParameter("q")));
    resp.getWriter().print("<p>" + e + "</p>");                // EXPECT: REFUTED (the escape is undone)
  } }
