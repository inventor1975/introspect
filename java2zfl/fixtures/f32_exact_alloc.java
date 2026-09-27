public class F32 { abstract static class Base { abstract void action(String d) throws Exception; }
  static class Bad extends Base { void action(String d) throws Exception { Runtime.getRuntime().exec(d); } }
  static class Good extends Base { void action(String d) { } }
  public void doPost(HttpServletRequest request) throws Exception {
    String data = request.getParameter("x");
    Base b = new Bad();  b.action(data);      // EXPECT: REFUTED (allocated exactly as Bad)
    Base g = new Good(); g.action(data);      // EXPECT: nothing (Good.action has no sink)
  } }
