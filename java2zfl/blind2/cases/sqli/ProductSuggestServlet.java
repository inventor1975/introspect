package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/products/suggest")
public class ProductSuggestServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String prefix = request.getParameter("q");
        if (prefix == null || prefix.trim().length() < 2) {
            response.setContentType("application/json");
            response.getWriter().print("[]");
            return;
        }
        String sql = "SELECT id, price FROM products WHERE active = true AND name ILIKE ? ORDER BY name LIMIT 10";

        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.open(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, prefix.trim() + "%");
            try (ResultSet rs = ps.executeQuery()) {
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
            }
        } catch (SQLException e) {
            throw new ServletException("suggest failed", e);
        }
    }
}
