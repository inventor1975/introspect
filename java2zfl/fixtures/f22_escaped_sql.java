public class C08 { public void doPost(HttpServletRequest request, java.sql.Statement st, HttpServletResponse response) throws Exception {
  String param = request.getParameter("x");
  String bar = org.springframework.web.util.HtmlUtils.htmlEscape(param);
  st.executeQuery("select " + bar);
  response.getWriter().print(bar); } }
