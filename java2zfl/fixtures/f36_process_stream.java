public class F36 { public void doPost(HttpServletRequest request, HttpServletResponse response) throws Exception {
    Process p = Runtime.getRuntime().exec("uptime");
    java.io.BufferedReader r = new java.io.BufferedReader(new java.io.InputStreamReader(p.getInputStream()));
    response.getWriter().println(r.readLine());   // EXPECT: OPEN (a process stream is not the request: unknown, not T)
  } }
