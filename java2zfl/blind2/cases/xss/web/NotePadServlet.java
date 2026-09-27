package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@WebServlet("/scratch")
public class NotePadServlet extends HttpServlet {

    private static final Map<String, String> NOTES = new ConcurrentHashMap<>();

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String board = request.getParameter("board");
        String text = request.getParameter("text");
        if (board != null && text != null) {
            NOTES.put(board, text);
        }
        response.sendRedirect("/scratch?board=" + java.net.URLEncoder.encode(board == null ? "main" : board, "UTF-8"));
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String board = request.getParameter("board");
        String text = NOTES.getOrDefault(board == null ? "main" : board, "(empty)");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Shared scratch pad</h2>");
        out.println("<div class=\"pad\">" + text + "</div>");
        out.println("<form method=\"post\"><textarea name=\"text\"></textarea><button>Save</button></form>");
        out.println("</body></html>");
    }
}
