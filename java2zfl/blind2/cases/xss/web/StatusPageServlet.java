package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletOutputStream;

@WebServlet("/jobs/status")
public class StatusPageServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String job = request.getParameter("job");
        String html = "<html><body><h3>Job " + job + "</h3><p>Status: queued</p>"
                + "<meta http-equiv=\"refresh\" content=\"5\"></body></html>";
        byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
        response.setContentType("text/html;charset=UTF-8");
        ServletOutputStream os = response.getOutputStream();
        os.write(bytes);
        os.flush();
    }
}
