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

@WebServlet("/catalog/supplier")
public class CatalogSupplierServlet extends HttpServlet {

    private ProductDao products;

    @Override
    public void init() throws ServletException {
        products = new ProductDao(DataSources.lookup("jdbc/shop"));
    }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String supplier = req.getParameter("supplier");
        long supplierId;
        try {
            supplierId = Long.parseLong(supplier);
        } catch (NumberFormatException e) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        List<String> skus;
        try {
            skus = products.findSkusBySupplier(supplierId);
        } catch (SQLException e) {
            throw new ServletException(e);
        }
        resp.setContentType("text/plain");
        resp.getWriter().println(skus.size() + " products");
    }
}
