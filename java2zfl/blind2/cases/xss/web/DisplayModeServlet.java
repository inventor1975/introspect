package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reader")
public class DisplayModeServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String requested = request.getParameter("mode");
        String mode = "dark".equals(requested) ? "dark" : "light";
        String font = request.getParameter("font");
        String fontClass = (font != null && font.equals("serif")) ? "font-serif" : "font-sans";
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html class=\"" + mode + " " + fontClass + "\"><body><article id=\"reader\"></article></body></html>");
    }
}
