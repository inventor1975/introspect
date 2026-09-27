package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/visitors/note")
public class GuestNoteServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String note = request.getParameter("note");
        if (note == null) {
            note = "";
        }
        String shown = note.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h3>Your note</h3>");
        out.println("<p class=\"note\">" + shown + "</p>");
        out.println("</body></html>");
    }
}
