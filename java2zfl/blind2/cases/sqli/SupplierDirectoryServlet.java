package blind2.sqli;

import blind2.sqli.support.Db;
import blind2.sqli.support.Params;
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

@WebServlet("/suppliers")
public class SupplierDirectoryServlet extends HttpServlet {

    private static final int PAGE_SIZE = 25;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String country = Params.text(req, "country", "DE");
        int page = Math.max(0, Params.integer(req, "page", 0));

        String sql = "SELECT id, rating FROM suppliers WHERE country_code = '" + country + "'"
                + " ORDER BY rating DESC LIMIT " + PAGE_SIZE + " OFFSET " + (page * PAGE_SIZE);

        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + ";" + rs.getInt(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
