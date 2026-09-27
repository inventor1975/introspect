public class C12 { public void doPost(HttpServletRequest request, HttpServletResponse response) throws Exception {
  String param = request.getParameter("x");
  StringBuilder sb = new StringBuilder();
  sb.append("a").append(param);
  java.util.List<String> argList = new java.util.ArrayList<String>();
  argList.add("sh"); argList.add("-c"); argList.add("echo " + param);
  ProcessBuilder pb = new ProcessBuilder();
  pb.command(argList);
  response.getWriter().printf("x %s", sb.toString()); } }
