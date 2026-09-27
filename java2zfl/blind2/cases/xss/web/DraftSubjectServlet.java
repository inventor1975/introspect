package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.HashMap;
import java.util.Map;
import blind2.xss.support.Markup;

@WebServlet("/inbox/draft")
public class DraftSubjectServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Map<String, Object> draft = new HashMap<>();
        draft.put("subject", request.getParameter("subject"));
        draft.put("savedAt", java.time.LocalTime.now().withNano(0));
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"draft\"><h4>" + Markup.text(draft.get("subject")) + "</h4>");
        out.println("<small>Saved at " + Markup.text(draft.get("savedAt")) + "</small></div>");
    }
}
