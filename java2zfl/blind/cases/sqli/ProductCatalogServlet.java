package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog")
public class ProductCatalogServlet extends HttpServlet {

    private static final int PAGE_SIZE = 25;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String sort = request.getParameter("sort");
        if (sort == null || sort.isEmpty()) {
            sort = "name";
        }
        StringBuilder sql = new StringBuilder("SELECT sku, name, price FROM products WHERE active = TRUE");
        sql.append(" ORDER BY ").append(sort);
        sql.append(" LIMIT ").append(PAGE_SIZE);

        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            ResultSet rs = st.executeQuery(sql.toString());
            while (rs.next()) {
                out.printf("%s %s %s%n", rs.getString("sku"), rs.getString("name"), rs.getBigDecimal("price"));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
