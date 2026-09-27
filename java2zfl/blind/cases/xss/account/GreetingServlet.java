package blind.xss.account;

import java.io.IOException;
import java.time.LocalTime;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/greeting")
public class GreetingServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String first = req.getParameter("first");
        String html = buildGreeting(first == null ? "there" : first.trim(), LocalTime.now());
        resp.setContentType("text/html;charset=UTF-8");
        resp.getWriter().write(html);
    }

    private String buildGreeting(String who, LocalTime now) {
        String part;
        if (now.getHour() < 12) {
            part = "morning";
        } else if (now.getHour() < 18) {
            part = "afternoon";
        } else {
            part = "evening";
        }
        return "<p class=\"greeting\">Good " + part + ", " + who + "!</p>";
    }
}
