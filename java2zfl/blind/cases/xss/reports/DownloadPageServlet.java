package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/download")
public class DownloadPageServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String file = req.getParameter("file");
        if (file == null) {
            file = "report.csv";
        }
        String encoded = URLEncoder.encode(file, StandardCharsets.UTF_8);
        String link = "/files/download?name=" + encoded;
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        out.println("<p>Your download will start shortly. If it does not, use this link:</p>");
        out.println("<p><a href=\"" + link + "\">" + link + "</a></p>");
        out.println("<p class=\"hint\">Requested file: <code>" + encoded + "</code></p>");
    }
}
