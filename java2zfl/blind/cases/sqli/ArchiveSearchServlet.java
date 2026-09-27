package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/archive/search")
public class ArchiveSearchServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        List<String> conditions = new ArrayList<>();
        conditions.add("deleted = FALSE");
        String author = request.getParameter("author");
        if (author != null && !author.isBlank()) {
            conditions.add("author = '" + author + "'");
        }
        String year = request.getParameter("year");
        if (year != null && year.matches("\\d{4}")) {
            conditions.add("EXTRACT(YEAR FROM created_at) = " + year);
        }
        String where = conditions.stream().collect(Collectors.joining(" AND ", " WHERE ", ""));
        PrintWriter out = response.getWriter();
        try (Connection conn = Db.connect(); Statement st = conn.createStatement();
             ResultSet rs = st.executeQuery("SELECT id, title FROM documents" + where)) {
            while (rs.next()) {
                out.println(rs.getLong(1) + " " + rs.getString(2));
            }
        } catch (SQLException e) {
            throw new ServletException(e);
        }
    }
}
