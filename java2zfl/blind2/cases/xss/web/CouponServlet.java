package blind2.xss.web;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.lang3.StringUtils;

@WebServlet("/checkout/coupon")
public class CouponServlet extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String code = StringUtils.trim(request.getParameter("code"));
        response.setContentType("text/html;charset=UTF-8");
        PrintWriter out = response.getWriter();
        if (!StringUtils.isAlphanumeric(code)) {
            out.println("<div class=\"coupon err\">That code does not look right.</div>");
            return;
        }
        out.println("<div class=\"coupon\">Code <b>" + code.toUpperCase() + "</b> applied.</div>");
    }
}
