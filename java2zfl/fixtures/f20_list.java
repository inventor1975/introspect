public class C06 { public void doPost(HttpServletRequest request, java.sql.Statement st) throws Exception {
  String param = request.getParameter("x");
  java.util.List<String> valuesList = new java.util.ArrayList<String>();
  valuesList.add("safe"); valuesList.add(param); valuesList.add("moresafe");
  valuesList.remove(0);
  String bar = valuesList.get(1);
  String bad = valuesList.get(0);
  st.executeQuery("select " + bar);
  st.execute("select " + bad); } }
