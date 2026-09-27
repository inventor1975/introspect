package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

@WebServlet("/me/card")
public class ProfileCardServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null) {
            response.sendRedirect("/login");
            return;
        }
        Object name = session.getAttribute("displayName");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><div class=\"card\">");
        out.println("<span class=\"who\">" + (name == null ? "Member" : name) + "</span>");
        out.println("<span class=\"sid\">" + session.getId().substring(0, 6) + "</span>");
        out.println("</div></body></html>");
    }
}
