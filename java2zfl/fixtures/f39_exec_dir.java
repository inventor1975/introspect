public class F39 { public void doPost(HttpServletRequest request) throws Exception {
    String[] args = {"sh", "-c", "ls"};
    Runtime.getRuntime().exec(args, new String[]{"a=b"}, new java.io.File(System.getProperty("user.dir")));  // EXPECT: nothing (dir is not a command)
    Runtime.getRuntime().exec(args, new String[]{"a=" + request.getParameter("e")});                        // EXPECT: REFUTED (envp)
  } }
