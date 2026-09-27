package org.springframework.jdbc.support.rowset; public interface SqlRowSet { boolean next(); String getString(String c); int getInt(String c); }
