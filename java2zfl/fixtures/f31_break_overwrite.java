public class C17 { public void doPost(HttpServletRequest request) throws Exception {
  String param = "";
  java.util.Enumeration<String> names = request.getParameterNames();
  while (names.hasMoreElements()) { String name = names.nextElement();
     if (name.startsWith("x")) { param = name; break; }
     param = "safe"; }
  Runtime.getRuntime().exec(param); } }
