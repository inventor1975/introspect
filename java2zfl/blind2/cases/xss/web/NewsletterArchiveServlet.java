package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.HtmlFragments;

@WebServlet("/newsletter/archive-note")
public class NewsletterArchiveServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String subject = request.getParameter("subject");
        String note = request.getParameter("note");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.write("<html><body>");
        HtmlFragments.heading(out, subject == null ? "(no subject)" : subject);
        HtmlFragments.textParagraph(out, note == null ? "" : note);
        out.write("</body></html>");
    }
}
