public class C03 { public void doPost(HttpServletRequest request) throws Exception {
  String param = request.getParameter("x"); String bar;
  String guess = "ABC"; char t = guess.charAt(1);
  switch (t) { case 'A': bar = param; break; case 'B': bar = "bob"; break; case 'C': case 'D': bar = param; break; default: bar = "x"; }
  Runtime.getRuntime().exec(bar); } }
