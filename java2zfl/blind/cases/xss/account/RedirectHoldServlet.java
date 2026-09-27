package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/account/signed-out")
public class RedirectHoldServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String next = req.getParameter("next");
        String target = (next != null && next.startsWith("/") && !next.startsWith("//")) ? next : "/";
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<p>You have been signed out.</p>");
        out.println("<script>");
        out.println("setTimeout(function () { window.location.href = '" + Encode.forJavaScript(target) + "'; }, 2000);");
        out.println("</script>");
    }
}
