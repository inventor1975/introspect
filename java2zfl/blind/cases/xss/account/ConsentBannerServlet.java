package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/account/consent")
public class ConsentBannerServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String consentValue = null;
        Cookie[] cookies = req.getCookies();
        if (cookies != null) {
            for (Cookie c : cookies) {
                if ("consent".equals(c.getName())) {
                    consentValue = c.getValue();
                    break;
                }
            }
        }
        boolean granted = "granted".equals(consentValue);
        String state = granted ? "granted" : "pending";
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<div class=\"consent consent-" + state + "\" data-state=\"" + state + "\">");
        if (!granted) {
            out.println("We use cookies to improve your experience. <button id=\"accept\">Accept</button>");
        }
        out.println("</div>");
    }
}
