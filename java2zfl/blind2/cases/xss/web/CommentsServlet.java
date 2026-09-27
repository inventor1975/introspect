package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;
import java.util.Map;
import blind2.xss.support.DataSources;
import org.springframework.jdbc.core.JdbcTemplate;

@WebServlet("/articles/comments")
public class CommentsServlet extends HttpServlet {

    private JdbcTemplate jdbc;

    @Override
    public void init() throws ServletException {
        jdbc = new JdbcTemplate(DataSources.primary());
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        long articleId;
        try {
            articleId = Long.parseLong(request.getParameter("article"));
        } catch (NumberFormatException e) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        List<Map<String, Object>> rows = jdbc.queryForList(
                "SELECT author, body FROM comments WHERE article_id = ? ORDER BY created_at", articleId);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<section class=\"comments\">");
        for (Map<String, Object> row : rows) {
            out.println("<article><h4>" + row.get("author") + "</h4><div>" + row.get("body") + "</div></article>");
        }
        out.println("</section>");
    }
}
