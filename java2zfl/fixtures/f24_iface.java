public class C10 { interface Thing { String doSomething(String s); }
  public void doPost(HttpServletRequest request, Thing thing) throws Exception {
  String param = request.getParameter("x");
  String bar = thing.doSomething(param);
  Runtime.getRuntime().exec(bar); } }
