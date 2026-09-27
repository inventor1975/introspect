public class F37 { interface Thing { String doSomething(String s); }
  static class A implements Thing { public String doSomething(String s) { return s; } }
  static class B implements Thing { public String doSomething(String s) { if (s == null) return ""; return new StringBuilder(s).toString(); } }
  public void doPost(HttpServletRequest request, Thing thing) throws Exception {
    String bar = thing.doSomething(request.getParameter("x"));
    Runtime.getRuntime().exec(bar);             // EXPECT: REFUTED (every implementation in view passes it)
    Thing anon = pick();
    String c = anon.doSomething("ls");
    Runtime.getRuntime().exec(c);               // EXPECT: nothing (every implementation returns its argument or "")
  }
  Thing pick() { return new Thing() { public String doSomething(String s) { return s; } }; } }
