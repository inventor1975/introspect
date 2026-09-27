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

@WebServlet("/warehouse/bin")
public class WarehouseStockServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String bin = req.getParameter("bin");
        if (bin == null) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "bin required");
            return;
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            boolean hasRows = st.execute("SELECT sku_id, qty FROM stock WHERE bin_code = '" + bin.toUpperCase() + "'");
            if (hasRows) {
                try (ResultSet rs = st.getResultSet()) {
                    while (rs.next()) {
                        out.println(rs.getLong(1) + " x" + rs.getInt(2));
                    }
                }
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
