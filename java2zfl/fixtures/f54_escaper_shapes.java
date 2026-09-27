public class F54 {
  void h(HttpServletRequest req, HttpServletResponse resp, java.util.List<String> tags) throws Exception {
    String q = req.getParameter("q");
    String safe = q.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;");
    resp.getWriter().print("<p>" + safe + "</p>");             // clean: a hand-written HTML escaper
    String half = q.replace("<", "&lt;").replace(">", "&gt;").replace("x", "y");
    resp.getWriter().print("<p>" + half + "</p>");             // EXPECT: REFUTED (& is not escaped: not an escaper)
    String chips = java.util.Arrays.stream(req.getParameterValues("f"))
        .map(org.owasp.encoder.Encode::forHtml).collect(java.util.stream.Collectors.joining(" "));
    resp.getWriter().print("<div>" + chips + "</div>");       // clean: an escaper as a method reference
  } }
