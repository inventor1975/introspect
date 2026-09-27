package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.EscapingRenderer;
import blind2.xss.support.Renderer;

@WebServlet("/shelf/label")
public class PriceTagServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String product = request.getParameter("product");
        String price = request.getParameter("price");
        Renderer renderer = new EscapingRenderer();
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"tag\"><span class=\"name\">" + renderer.render(product) + "</span>");
        out.println("<span class=\"price\">" + renderer.render(price) + "</span></div>");
    }
}
