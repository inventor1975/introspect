import org.apache.commons.text.StringEscapeUtils;
public class F44 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    java.io.PrintWriter out = resp.getWriter();
    String q = req.getParameter("q");
    String e = StringEscapeUtils.escapeHtml4(q);
    out.println("<p>" + e + "</p>");                          // clean: HTML text
    out.println("<input value=\"" + e + "\">");               // clean: double-quoted attribute
    out.println("<input value='" + e + "'>");                 // EXPECT: REFUTED (escapeHtml4 leaves ')
    out.println("<a href=\"" + e + "\">x</a>");               // EXPECT: REFUTED (javascript: survives)
    out.println("<script>");
    out.println("var s = \"" + StringEscapeUtils.escapeEcmaScript(q) + "\";");   // clean: a JS string
    out.println("location.href = '" + StringEscapeUtils.escapeEcmaScript(q) + "';"); // EXPECT: REFUTED (a URL)
    out.println("</script>");
  } }
