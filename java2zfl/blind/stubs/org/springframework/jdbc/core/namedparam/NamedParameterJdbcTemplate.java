package org.springframework.jdbc.core.namedparam; import java.util.*; public class NamedParameterJdbcTemplate {
 public NamedParameterJdbcTemplate(javax.sql.DataSource ds){}
 public <T> List<T> query(String sql, Map<String,?> p, org.springframework.jdbc.core.RowMapper<T> m){return null;}
 public List<Map<String,Object>> queryForList(String sql, Map<String,?> p){return null;} public int update(String sql, Map<String,?> p){return 0;} }
