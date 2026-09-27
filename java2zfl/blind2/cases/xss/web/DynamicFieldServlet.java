package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.lang.reflect.Method;

@WebServlet("/forms/field")
public class DynamicFieldServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String accessor = getInitParameter("valueAccessor");
        if (accessor == null) {
            accessor = "getParameter";
        }
        Object value;
        try {
            Method m = HttpServletRequest.class.getMethod(accessor, String.class);
            value = m.invoke(request, "field");
        } catch (ReflectiveOperationException e) {
            throw new ServletException(e);
        }
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<label>Current value</label><output>" + value + "</output>");
    }
}
