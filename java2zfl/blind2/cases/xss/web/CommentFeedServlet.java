package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.DataSources;
import org.owasp.encoder.Encode;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.rowset.SqlRowSet;

@WebServlet("/threads/latest")
public class CommentFeedServlet extends HttpServlet {

    private JdbcTemplate jdbc;

    @Override
    public void init() throws ServletException {
        jdbc = new JdbcTemplate(DataSources.primary());
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String board = request.getParameter("board");
        SqlRowSet rs = jdbc.queryForRowSet(
                "SELECT author, body FROM posts WHERE board = ? ORDER BY id DESC LIMIT 20", board);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<h3>Latest in " + Encode.forHtml(board) + "</h3><ul>");
        while (rs.next()) {
            String author = rs.getString("author");
            String body = rs.getString("body");
            out.println("<li><b>" + Encode.forHtml(author) + "</b>: " + Encode.forHtml(body) + "</li>");
        }
        out.println("</ul>");
    }
}
