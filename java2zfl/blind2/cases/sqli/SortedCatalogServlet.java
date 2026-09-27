package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Objects;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog")
public class SortedCatalogServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String sort = Objects.requireNonNullElse(req.getParameter("sort"), "name");
        String column;
        switch (sort) {
            case "price":
                column = "unit_price";
                break;
            case "newest":
                column = "created_at DESC";
                break;
            case "rating":
                column = "avg_rating DESC NULLS LAST";
                break;
            default:
                column = sort;
        }

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id FROM products WHERE active = true ORDER BY " + column + " LIMIT 60")) {
            while (rs.next()) {
                out.println(rs.getLong(1));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
