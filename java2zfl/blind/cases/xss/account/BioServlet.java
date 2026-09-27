package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/account/bio")
public class BioServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String tagline = req.getParameter("tagline");
        String bio = req.getParameter("bio");
        tagline = tagline == null ? "" : tagline;
        bio = bio == null ? "" : bio;
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<form method='post' action='/account/bio'>");
        out.println("  <input type='text' name='tagline' value='" + Encode.forHtmlAttribute(tagline) + "'>");
        out.println("  <textarea name='bio' rows='6'>" + Encode.forHtml(bio) + "</textarea>");
        out.println("  <button type='submit'>Save</button>");
        out.println("</form>");
    }
}
