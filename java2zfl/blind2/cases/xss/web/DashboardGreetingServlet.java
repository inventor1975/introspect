package blind2.xss.web;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.LayoutServlet;

@WebServlet("/dashboard/widget")
public class DashboardGreetingServlet extends LayoutServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String widget = request.getParameter("widget");
        writePage(response, widget == null ? "Widget" : widget, "<div class=\"widget\" id=\"w1\"></div>");
    }
}
