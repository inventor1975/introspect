public class C13 { public void doPost(HttpServletRequest request) throws Exception {
  String bar;
  try { bar = request.getParameter("x"); } catch (Exception e) { bar = "safe"; }
  String s = "a"; s += request.getParameter("y");
  Runtime.getRuntime().exec(bar);
  Runtime.getRuntime().exec(s); } }
