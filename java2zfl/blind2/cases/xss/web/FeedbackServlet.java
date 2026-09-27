package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.BufferedReader;

@WebServlet("/feedback")
public class FeedbackServlet extends HttpServlet {

    private static final int MAX_CHARS = 4000;

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        StringBuilder body = new StringBuilder();
        try (BufferedReader reader = request.getReader()) {
            String line;
            while ((line = reader.readLine()) != null && body.length() < MAX_CHARS) {
                body.append(line).append('\n');
            }
        }
        String text = body.toString().trim();
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body><h2>Thank you!</h2>");
        out.println("<p>We received the following feedback:</p>");
        out.println("<blockquote>" + text + "</blockquote>");
        out.println("</body></html>");
    }
}
