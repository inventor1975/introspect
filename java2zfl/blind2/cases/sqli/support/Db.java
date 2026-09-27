package blind2.sqli.support;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class Db {

    private static final String URL = "jdbc:postgresql://db.internal:5432/shop";
    private static final String USER = "shop_app";

    private Db() {
    }

    public static Connection open() throws SQLException {
        return DriverManager.getConnection(URL, USER, System.getenv("SHOP_DB_PASSWORD"));
    }
}
