package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/avatar")
public class AvatarServlet extends HttpServlet {

    private static final int DEFAULT_SIZE = 64;
    private static final int MIN_SIZE = 16;
    private static final int MAX_SIZE = 512;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sizeParam = req.getParameter("size");
        int size;
        try {
            size = Integer.parseInt(sizeParam);
        } catch (NumberFormatException e) {
            size = DEFAULT_SIZE;
        }
        size = Math.min(Math.max(size, MIN_SIZE), MAX_SIZE);

        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.print("<div class=\"avatar\" style=\"width:" + size + "px;height:" + size + "px\">");
        out.print("<img src=\"/static/avatar-default.png\" width=" + size + " height=" + size + " alt=\"\">");
        out.println("</div>");
    }
}
