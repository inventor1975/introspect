package blind.xss.account;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;

@WebServlet("/account/nickname")
public class NicknameServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String nick = req.getParameter("nickname");
        if (nick == null) {
            nick = "";
        }
        String escaped = StringEscapeUtils.escapeHtml4(nick);
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<form method='post' action='/account/nickname'>");
        out.println("  <label for='nick'>Nickname</label>");
        out.println("  <input id='nick' type='text' name='nickname' value='" + escaped + "' maxlength='30'>");
        out.println("  <button type='submit'>Save</button>");
        out.println("</form>");
    }
}
