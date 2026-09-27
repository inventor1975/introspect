public class F34 { public void doPost(HttpServletRequest request, HttpServletResponse response) throws Exception {
    String data = request.getParameter("x");
    response.sendError(404, "<br>no page " + data);   // EXPECT: OPEN (does the container escape the error page?)
    response.sendError(404, "<br>no page");           // EXPECT: nothing
  } }
