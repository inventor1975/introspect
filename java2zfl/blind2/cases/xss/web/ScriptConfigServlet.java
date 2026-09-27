package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;

@WebServlet("/app")
public class ScriptConfigServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String initialQuery = request.getParameter("q");
        if (initialQuery == null) {
            initialQuery = "";
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<!DOCTYPE html><html><head>");
        out.println("<script>");
        out.println("  window.APP_CONFIG = { initialQuery: '" + Encode.forJavaScript(initialQuery) + "', pageSize: 25 };");
        out.println("</script>");
        out.println("<script src=\"/static/app.js\"></script></head><body><div id=\"root\"></div></body></html>");
    }
}
