public class C02 { public void doPost(HttpServletRequest request, String sel) throws Exception {
  String param = request.getParameter("x"); String bar;
  switch (sel) { case "a": bar = param; break; case "b": bar = "bob"; break; default: bar = "d"; }
  Runtime.getRuntime().exec(bar); } }
