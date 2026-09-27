package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Set;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/sorted")
public class ProductSortServlet extends HttpServlet {

    private static final Set<String> SORTABLE = Set.of("name", "price", "created_at");

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String sort = request.getParameter("sort");
        if (sort == null) {
            sort = "name";
        }
        if (!SORTABLE.contains(sort)) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST, "unsupported sort column");
            return;
        }
        StringBuilder sql = new StringBuilder("SELECT sku, name, price FROM products WHERE active = TRUE");
        sql.append(" ORDER BY ").append(sort).append(" LIMIT 25");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql.toString())) {
            while (rs.next()) {
                out.printf("%s %s %s%n", rs.getString("sku"), rs.getString("name"), rs.getBigDecimal("price"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
