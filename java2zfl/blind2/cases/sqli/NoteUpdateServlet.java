package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/notes/update")
public class NoteUpdateServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        long noteId;
        try {
            noteId = Long.parseLong(req.getParameter("id"));
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        String text = req.getParameter("text");
        if (text == null) {
            text = "";
        }
        try (Connection conn = Db.open(); Statement st = conn.createStatement()) {
            long updated = st.executeLargeUpdate("UPDATE notes SET body = '" + text + "', edited_at = now() WHERE id = " + noteId);
            resp.setStatus(updated == 1 ? HttpServletResponse.SC_OK : HttpServletResponse.SC_NOT_FOUND);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
