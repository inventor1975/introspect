public class F40 { public void doPost(HttpServletRequest request, HttpServletResponse response) throws Exception {
    Object[] obj = {"a", "b"};
    response.getWriter().printf(java.util.Locale.US, "x %s", obj);          // EXPECT: nothing (library constant)
    response.getWriter().printf(java.util.Locale.US, request.getParameter("f"), obj);  // EXPECT: REFUTED
    response.getWriter().print(Config.current);                              // EXPECT: OPEN (a lower-case field of an unknown class)
  } }
