package blind.sqli;

import blind.sqli.support.Db;
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Map;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/survey/submit")
public class FeedbackServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Map<String, String[]> answers = request.getParameterMap();
        String surveyId = "2026-q3";
        try (Connection conn = Db.connect(); Statement st = conn.createStatement()) {
            conn.setAutoCommit(false);
            for (Map.Entry<String, String[]> e : answers.entrySet()) {
                String question = e.getKey();
                if (!question.startsWith("q")) {
                    continue;
                }
                for (String answer : e.getValue()) {
                    st.addBatch("INSERT INTO survey_answers (survey, question, answer) VALUES ('"
                            + surveyId + "', '" + question + "', '" + answer + "')");
                }
            }
            st.executeBatch();
            conn.commit();
        } catch (SQLException ex) {
            throw new ServletException(ex);
        }
        response.sendRedirect("/survey/thanks");
    }
}
