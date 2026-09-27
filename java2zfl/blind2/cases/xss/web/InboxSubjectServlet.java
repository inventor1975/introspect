package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.Markup;

@WebServlet("/inbox/compose-preview")
public class InboxSubjectServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String subject = request.getParameter("subject");
        int recipients = request.getParameterValues("to") == null ? 0 : request.getParameterValues("to").length;
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"preview\"><h4>" + Markup.text(subject) + "</h4>");
        out.println("<span>" + Markup.text(recipients) + " recipient(s)</span></div>");
    }
}
