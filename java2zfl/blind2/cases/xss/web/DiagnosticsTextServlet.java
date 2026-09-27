package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/diag/echo")
public class DiagnosticsTextServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String probe = request.getParameter("probe");
        response.setContentType("text/plain;charset=UTF-8");
        response.setHeader("X-Content-Type-Options", "nosniff");
        PrintWriter out = response.getWriter();
        out.println("status: ok");
        out.println("remote: " + request.getRemoteAddr());
        out.println("probe: " + probe);
    }
}
