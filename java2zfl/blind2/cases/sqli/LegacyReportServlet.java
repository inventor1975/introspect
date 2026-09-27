package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/legacy")
public class LegacyReportServlet extends HttpServlet {

    private final Properties queries = new Properties();

    @Override
    public void init() throws ServletException {
        try (InputStream in = LegacyReportServlet.class.getResourceAsStream("/reports.properties")) {
            if (in == null) {
                throw new ServletException("reports.properties not found on classpath");
            }
            queries.load(in);
        } catch (IOException e) {
            throw new ServletException(e);
        }
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String report = req.getParameter("report");
        String sql = report == null ? null : queries.getProperty("report." + report + ".sql");
        if (sql == null) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND, "no such report");
            return;
        }
        resp.setContentType("text/plain");
        PrintWriter out = resp.getWriter();
        try (Connection conn = Db.open();
             Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery(sql)) {
            int rows = 0;
            while (rs.next()) {
                rows++;
            }
            out.println(rows + " rows");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
