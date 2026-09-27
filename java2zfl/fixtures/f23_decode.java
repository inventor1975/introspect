public class C09 { public void doPost(HttpServletRequest request) throws Exception {
  String param = "";
  if (request.getHeader("x") != null) param = request.getHeader("x");
  param = java.net.URLDecoder.decode(param, "UTF-8");
  Runtime.getRuntime().exec(param); } }
