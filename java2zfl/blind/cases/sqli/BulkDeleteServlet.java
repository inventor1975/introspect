package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/drafts/delete")
public class BulkDeleteServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String[] ids = request.getParameterValues("id");
        if (ids == null || ids.length == 0) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String idList = String.join(",", ids);
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            int removed = st.executeUpdate("DELETE FROM drafts WHERE id IN (" + idList + ") AND published = FALSE");
            response.getWriter().println(removed + " drafts removed");
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
