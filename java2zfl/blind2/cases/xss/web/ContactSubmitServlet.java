package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.logging.Logger;

@WebServlet("/contact")
public class ContactSubmitServlet extends HttpServlet {

    private static final Logger AUDIT = Logger.getLogger("contact.audit");

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String name = request.getParameter("name");
        String message = request.getParameter("message");
        String archived = "<div class=\"msg\"><b>" + name + "</b><p>" + message + "</p></div>";
        AUDIT.info(archived);

        String reply = "<html><body><h2>Thanks for getting in touch</h2>"
                + "<p>We usually answer within one business day.</p></body></html>";
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println(reply);
    }
}
