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
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/warehouse/stock")
public class WarehouseStockServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String bin = StringEscapeUtils.escapeHtml4(request.getParameter("bin"));
        String sql = "SELECT sku, qty FROM bin_contents WHERE bin_code = '" + bin + "'";
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        out.println("<h2>Bin " + bin + "</h2><ul>");
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println("<li>" + StringEscapeUtils.escapeHtml4(rs.getString("sku")) + ": " + rs.getInt("qty") + "</li>");
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        out.println("</ul>");
    }
}
