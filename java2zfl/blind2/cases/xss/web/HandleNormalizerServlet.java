package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/profile/handle")
public class HandleNormalizerServlet extends HttpServlet {

    static String normalize(String raw) {
        StringBuilder sb = new StringBuilder();
        for (char c : raw.toCharArray()) {
            if (Character.isLetterOrDigit(c) && c < 128) {
                sb.append(Character.toLowerCase(c));
            } else if (c == '_' || c == '.') {
                sb.append(c);
            }
        }
        return sb.toString();
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String requested = request.getParameter("handle");
        String handle = normalize(requested == null ? "" : requested);
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<p>Your public handle will be <b>@" + handle + "</b></p>");
    }
}
