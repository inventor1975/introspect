public class C01 { public void doPost(HttpServletRequest request) throws Exception {
  String param = request.getParameter("x");
  String bar = new Test().doSomething(request, param);
  Runtime.getRuntime().exec(bar); }
  private class Test { public String doSomething(HttpServletRequest request, String param) throws Exception { String bar = param; return bar; } } }
