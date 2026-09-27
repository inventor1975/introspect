package org.springframework.jdbc.core; import java.util.*; public class JdbcTemplate {
 public JdbcTemplate(){} public JdbcTemplate(javax.sql.DataSource ds){}
 public void execute(String sql){} public int update(String sql, Object... args){return 0;} public int[] batchUpdate(String... sql){return null;}
 public <T> List<T> query(String sql, RowMapper<T> m){return null;} public <T> List<T> query(String sql, RowMapper<T> m, Object... args){return null;}
 public <T> List<T> query(String sql, Object[] args, RowMapper<T> m){return null;}
 public List<Map<String,Object>> queryForList(String sql, Object... args){return null;} public <T> List<T> queryForList(String sql, Class<T> t, Object... args){return null;}
 public Map<String,Object> queryForMap(String sql, Object... args){return null;}
 public <T> T queryForObject(String sql, Class<T> t){return null;} public <T> T queryForObject(String sql, Class<T> t, Object... args){return null;}
 public <T> T queryForObject(String sql, RowMapper<T> m, Object... args){return null;}
 public org.springframework.jdbc.support.rowset.SqlRowSet queryForRowSet(String sql, Object... args){return null;} }
