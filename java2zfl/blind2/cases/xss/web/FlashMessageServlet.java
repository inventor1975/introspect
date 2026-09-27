package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/settings/save")
public class FlashMessageServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String nickname = request.getParameter("nickname");
        request.setAttribute("flash", "Saved settings for " + nickname);
        render(request, response);
    }

    private void render(HttpServletRequest request, HttpServletResponse response) throws IOException {
        Object flash = request.getAttribute("flash");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        if (flash != null) {
            out.println("<div class=\"flash\">" + flash + "</div>");
        }
        out.println("<form method=\"post\"><input name=\"nickname\"></form></body></html>");
    }
}
