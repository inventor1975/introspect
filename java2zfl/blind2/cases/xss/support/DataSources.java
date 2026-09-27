package blind2.xss.support;

import javax.sql.DataSource;

/** Holds the pool created at startup by the application listener. */
public final class DataSources {

    private static volatile DataSource primary;

    private DataSources() {
    }

    public static void register(DataSource ds) {
        primary = ds;
    }

    public static DataSource primary() {
        if (primary == null) {
            throw new IllegalStateException("datasource not initialised");
        }
        return primary;
    }
}
