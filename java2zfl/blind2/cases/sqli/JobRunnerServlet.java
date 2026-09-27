package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/admin/jobs/run")
public class JobRunnerServlet extends HttpServlet {

    private static final Map<String, String> PROCEDURES = Map.of(
            "reindex", "maint_reindex_catalog",
            "expire-carts", "maint_expire_carts",
            "recalc-ratings", "maint_recalc_ratings");

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String job = req.getParameter("job");
        String procedure = job == null ? null : PROCEDURES.get(job);
        if (procedure == null) {
            resp.sendError(HttpServletResponse.SC_NOT_FOUND, "unknown job");
            return;
        }
        try (Connection conn = Db.open();
             CallableStatement cs = conn.prepareCall("{call " + procedure + "()}")) {
            cs.execute();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().println(job + " started");
    }
}
