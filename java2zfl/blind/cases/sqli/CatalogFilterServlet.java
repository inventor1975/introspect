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
import org.owasp.encoder.Encode;

@WebServlet("/catalog/category")
public class CatalogFilterServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String categoryId = Encode.forHtml(request.getParameter("categoryId"));
        String sql = "SELECT p.name, p.price FROM products p JOIN product_categories pc ON pc.product_id = p.id"
                + " WHERE pc.category_id = " + categoryId;
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println("<p>" + Encode.forHtml(rs.getString(1)) + "</p>");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
