public class C04 { public void doPost(HttpServletRequest request) throws Exception {
  String param = request.getParameter("x");
  int num = 106;
  String bar = (7 * 18) + num > 200 ? "This_should_always_happen" : param;
  String b2 = (7 * 18) + num < 200 ? "no" : param;
  Runtime.getRuntime().exec(bar);
  Runtime.getRuntime().exec(b2); } }
