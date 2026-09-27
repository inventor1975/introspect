package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import blind2.xss.support.TextUtil;

@WebServlet("/shipping/label-preview")
public class AddressLabelServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String recipient = TextUtil.escape(request.getParameter("recipient"));
        String street = TextUtil.escape(request.getParameter("street"));
        String city = TextUtil.escape(request.getParameter("city"));
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        out.println("<div class=\"label\" data-recipient=\"" + recipient + "\">");
        out.println(recipient + "<br>" + street + "<br>" + city);
        out.println("</div>");
    }
}
