public class F50 {
  void h(HttpServletRequest req, HttpServletResponse resp) throws Exception {
    byte[] raw = java.util.Base64.getDecoder().decode(req.getParameter("p"));
    resp.getOutputStream().write(raw);                         // EXPECT: REFUTED (byte[] holds text; was clean)
    int[] ids = {1, 2};
    resp.getWriter().print("n=" + ids.length);                 // clean
  } }
