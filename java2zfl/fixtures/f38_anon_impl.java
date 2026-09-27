public class F38 { interface Thing { String doSomething(String s); }
  static class A implements Thing { public String doSomething(String s) { return "safe"; } }
  Thing pick(HttpServletRequest r) { return new Thing() { public String doSomething(String s) { return r.getParameter("x"); } }; }
  public void doPost(HttpServletRequest request, Thing thing) throws Exception {
    Runtime.getRuntime().exec(thing.doSomething("ls"));   // EXPECT: OPEN (A is clean, the anonymous one is not)
  } }
