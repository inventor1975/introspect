public class C11 { String h(String s) { String r = helperLib.f(s); return r; }
  public void doPost(HttpServletRequest request) throws Exception {
  String bar = h(request.getParameter("x"));
  Runtime.getRuntime().exec(bar); } }
