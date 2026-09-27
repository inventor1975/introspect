package blind.sqli;

import blind.sqli.support.Db;
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

@WebServlet("/contacts/import")
public class CsvImportServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Part upload = request.getPart("file");
        int imported = 0;
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             BufferedReader reader = new BufferedReader(
                     new InputStreamReader(upload.getInputStream(), StandardCharsets.UTF_8))) {
            String header = reader.readLine();
            if (header == null) {
                response.sendError(HttpServletResponse.SC_BAD_REQUEST, "empty file");
                return;
            }
            String line;
            while ((line = reader.readLine()) != null) {
                String[] cols = line.split(",", -1);
                if (cols.length < 2) {
                    continue;
                }
                st.addBatch("INSERT INTO contacts (full_name, email) VALUES ('" + cols[0] + "', '" + cols[1] + "')");
                imported++;
            }
            st.executeBatch();
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        response.getWriter().println(imported + " contacts imported");
    }
}
