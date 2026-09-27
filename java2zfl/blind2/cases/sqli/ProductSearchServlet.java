package blind2.sqli;

import blind2.sqli.support.Db;
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

@WebServlet("/products/search")
public class ProductSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String term = request.getParameter("q");
        if (term == null) {
            term = "";
        }
        String sql = "SELECT id, price FROM products WHERE active = true AND name ILIKE '%" + term.trim()
                + "%' ORDER BY name LIMIT 50";

        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            out.print("[");
            boolean first = true;
            while (rs.next()) {
                if (!first) {
                    out.print(",");
                }
                out.print("{\"id\":" + rs.getLong("id") + ",\"price\":" + rs.getBigDecimal("price") + "}");
                first = false;
            }
            out.print("]");
        } catch (SQLException e) {
            throw new ServletException("product search failed", e);
        }
    }
}
