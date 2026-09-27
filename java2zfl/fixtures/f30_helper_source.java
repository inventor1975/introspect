public class C16 { static class SeparateClassRequest { private HttpServletRequest r; SeparateClassRequest(HttpServletRequest r){this.r=r;}
    public String getTheParameter(String p) { return r.getParameter(p); } }
  public void doPost(HttpServletRequest request) throws Exception {
  SeparateClassRequest scr = new SeparateClassRequest(request);
  String param = scr.getTheParameter("x");
  Runtime.getRuntime().exec(param); } }
