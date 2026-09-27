package blind.xss.common;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.util.HtmlUtils;

/**
 * Common page chrome for the account area. Subclasses supply a plain-text title and a body fragment.
 */
public abstract class BasePageServlet extends HttpServlet {

    protected void render(HttpServletResponse resp, String title, String bodyHtml) throws IOException {
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        String safeTitle = HtmlUtils.htmlEscape(title);
        out.println("<!DOCTYPE html><html><head><title>" + safeTitle + " | My Account</title></head><body>");
        out.println("<header><nav><a href=\"/account\">Account</a> &middot; <a href=\"/logout\">Sign out</a></nav></header>");
        out.println("<main><h1>" + safeTitle + "</h1>");
        out.println(bodyHtml);
        out.println("</main></body></html>");
    }
}
