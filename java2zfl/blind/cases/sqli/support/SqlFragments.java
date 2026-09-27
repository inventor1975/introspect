package blind.sqli.support;

import java.util.Collections;

public final class SqlFragments {

    private SqlFragments() {
    }

    /** Builds a quoted LIKE literal such as '%abc%'. */
    public static String like(String term) {
        return "'%" + term.trim() + "%'";
    }

    /** Builds a LIKE pattern meant to be bound as a statement parameter. */
    public static String likeParam(String term) {
        return "%" + term.trim().toLowerCase() + "%";
    }

    public static String placeholders(int count) {
        return String.join(", ", Collections.nCopies(count, "?"));
    }
}
