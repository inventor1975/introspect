package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

@WebServlet("/motd")
public class MotdServlet extends HttpServlet {

    private static final Path MOTD_FILE = Path.of("/etc/portal/motd.html");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String motd = Files.exists(MOTD_FILE) ? Files.readString(MOTD_FILE, StandardCharsets.UTF_8) : "";
        String compact = request.getParameter("compact");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"motd" + ("1".equals(compact) ? " compact" : "") + "\">");
        out.println(motd);
        out.println("</div>");
    }
}
