package blind2.sqli;

import blind2.sqli.data.ProductDao;
import blind2.sqli.support.DataSources;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@WebServlet("/catalog/category")
public class CatalogBrowseServlet extends HttpServlet {

    private ProductDao products;

    @Override
    public void init() throws ServletException {
        products = new ProductDao(DataSources.lookup("jdbc/shop"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String category = req.getParameter("cat");
        if (category == null || category.isEmpty()) {
            resp.sendRedirect(req.getContextPath() + "/catalog");
            return;
        }
        List<String> skus;
        try {
            skus = products.findSkusByCategory(category);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        req.setAttribute("skuCount", skus.size());
        resp.setContentType("text/plain");
        resp.getWriter().println(skus.size() + " products");
    }
}
