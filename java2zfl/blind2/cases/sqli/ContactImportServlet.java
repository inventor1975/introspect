package blind2.sqli;

import blind2.sqli.support.Db;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

@WebServlet("/crm/contacts/import")
public class ContactImportServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        Object owner = req.getSession().getAttribute("userId");
        if (!(owner instanceof Long)) {
            resp.sendError(HttpServletResponse.SC_FORBIDDEN);
            return;
        }
        long ownerId = (Long) owner;
        Part upload = req.getPart("contacts");
        if (upload == null || upload.getSize() == 0) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST, "empty upload");
            return;
        }

        int imported = 0;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(upload.getInputStream(), StandardCharsets.UTF_8));
             Connection conn = Db.open();
             Statement st = conn.createStatement()) {
            String line = reader.readLine(); // header row
            while ((line = reader.readLine()) != null) {
                String[] cols = line.split(",", -1);
                if (cols.length < 3) {
                    continue;
                }
                imported += st.executeUpdate("INSERT INTO contacts(owner_id, full_name, email, phone) VALUES ("
                        + ownerId + ", '" + cols[0].trim() + "', '" + cols[1].trim() + "', '" + cols[2].trim() + "')");
            }
        } catch (SQLException e) {
            throw new ServletException("import failed after " + imported + " rows", e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().println(imported + " contacts imported");
    }
}
