public class C14 { public void doPost(HttpServletRequest request) throws Exception {
  javax.servlet.http.Cookie[] theCookies = request.getCookies();
  String param = "noCookieValueSupplied";
  if (theCookies != null) { for (javax.servlet.http.Cookie theCookie : theCookies) {
      if (theCookie.getName().equals("vector")) { param = java.net.URLDecoder.decode(theCookie.getValue(), "UTF-8"); break; } } }
  String[] args = {"sh", "-c", "echo"}; String[] env = {"x=" + param};
  Runtime.getRuntime().exec(args, env); } }
