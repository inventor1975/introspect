package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.EscapingRenderer;
import blind2.xss.support.PassThroughRenderer;
import blind2.xss.support.Renderer;

@WebServlet("/kb/preview")
public class MarkupPreviewServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        boolean htmlMode = "html".equals(request.getParameter("mode"));
        Renderer renderer = htmlMode ? new PassThroughRenderer() : new EscapingRenderer();
        String body = request.getParameter("body");
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<article class=\"kb\">" + renderer.render(body) + "</article>");
    }
}
