public class C07 { public void doPost(HttpServletRequest request, java.sql.Statement st) throws Exception {
  String param = request.getParameter("x");
  java.util.HashMap<String,Object> map = new java.util.HashMap<String,Object>();
  map.put("keyA", "a_Value"); map.put("keyB", param); map.put("keyC", "another");
  String bar = (String) map.get("keyA");
  String bad = (String) map.get("keyB");
  st.executeQuery("select " + bar);
  st.execute("select " + bad); } }
