package blind.sqli;

import java.time.Year;

final class ReportSqlBuilder {

    private static final String SELECT = "SELECT department, SUM(amount) AS total FROM expenses";

    private ReportSqlBuilder() {
    }

    static String forRegion(String region) {
        return SELECT + " WHERE region = '" + region + "' AND fiscal_year = " + Year.now().getValue()
                + " GROUP BY department";
    }

    static String forYear(int year) {
        return SELECT + " WHERE fiscal_year = " + year + " GROUP BY department";
    }

    static String forRegionParam() {
        return SELECT + " WHERE region = ? AND fiscal_year = ? GROUP BY department";
    }
}
