package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/board/preview")
public class MessageBoardServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String subject = request.getParameter("subject");
        String message = request.getParameter("message");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><div class=\"post\">");
        out.println("<h3>" + StringEscapeUtils.escapeXml11(subject == null ? "(no subject)" : subject) + "</h3>");
        out.println("<div class=\"msg\">" + StringEscapeUtils.escapeXml11(message == null ? "" : message) + "</div>");
        out.println("</div><button>Post</button></body></html>");
    }
}
