public class C05 { public void doPost(HttpServletRequest request, java.sql.Statement st) throws Exception {
  String param = request.getParameter("x"); String bar; int num = 86;
  if ((7 * 42) - num > 200) bar = "This_should_always_happen"; else bar = param;
  st.executeQuery("select " + bar); } }
