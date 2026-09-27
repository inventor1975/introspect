package blind2.sqli;

import javax.servlet.http.HttpServletRequest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.support.rowset.SqlRowSet;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class LegacyExportController {

    private final JdbcTemplate jdbc;

    public LegacyExportController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @RequestMapping(value = "/export/orders.csv", method = RequestMethod.GET, produces = "text/csv")
    @ResponseBody
    public String export(HttpServletRequest request) {
        String channel = request.getParameter("channel");
        if (channel == null) {
            channel = "web";
        }
        SqlRowSet rows = jdbc.queryForRowSet("SELECT id, total_cents FROM orders WHERE sales_channel = '" + channel
                + "' ORDER BY id");
        StringBuilder csv = new StringBuilder("id,total_cents\n");
        while (rows.next()) {
            csv.append(rows.getInt("id")).append(',').append(rows.getInt("total_cents")).append('\n');
        }
        return csv.toString();
    }
}
