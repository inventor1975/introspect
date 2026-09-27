package blind2.sqli.support;

import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.servlet.ServletException;
import javax.sql.DataSource;

public final class DataSources {

    private DataSources() {
    }

    public static DataSource lookup(String name) throws ServletException {
        try {
            return (DataSource) new InitialContext().lookup("java:comp/env/" + name);
        } catch (NamingException e) {
            throw new ServletException("JNDI lookup failed for " + name, e);
        }
    }
}
