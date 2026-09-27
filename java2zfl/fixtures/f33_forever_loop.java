public class F33 { public void doPost(HttpServletRequest request) throws Exception {
    String data;
    while (true) { data = "foo"; break; }      // runs once: data is "foo", never the unassigned value
    Runtime.getRuntime().exec(data);           // EXPECT: nothing
    String bad;
    while (true) { bad = request.getParameter("x"); break; }
    Runtime.getRuntime().exec(bad);            // EXPECT: REFUTED
  } }
