package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/billing/invoice")
public class InvoiceLookupServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        try {
            long number = Long.parseLong(request.getParameter("no"));
            out.println("<h2>Invoice #" + number + "</h2>");
            out.println("<iframe src=\"/billing/pdf?no=" + number + "\"></iframe>");
        } catch (NumberFormatException e) {
            out.println("<div class=\"error\">Could not read invoice number: " + e.getMessage() + "</div>");
        }
        out.println("</body></html>");
    }
}
