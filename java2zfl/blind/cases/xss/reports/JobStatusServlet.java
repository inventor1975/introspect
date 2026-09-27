package blind.xss.reports;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/reports/jobs/status")
public class JobStatusServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String jobParam = req.getParameter("job");
        resp.setContentType("text/html;charset=UTF-8");
        PrintWriter out = resp.getWriter();
        try {
            int jobId = Integer.parseInt(jobParam);
            out.println("<p>Export job #" + jobId + " is queued. This page refreshes automatically.</p>");
        } catch (NumberFormatException e) {
            out.println("<p class=\"error\">Could not read the job id (" + e.getMessage() + ").</p>");
        }
    }
}
