package javax.servlet.http; import java.util.*; public interface HttpServletRequest {
 String getParameter(String n); String[] getParameterValues(String n); Map<String,String[]> getParameterMap(); Enumeration<String> getParameterNames();
 String getHeader(String n); Enumeration<String> getHeaders(String n); Enumeration<String> getHeaderNames(); int getIntHeader(String n);
 Cookie[] getCookies(); String getQueryString(); String getRequestURI(); StringBuffer getRequestURL(); String getPathInfo(); String getServletPath(); String getContextPath();
 String getMethod(); String getRemoteAddr(); String getRemoteUser(); String getContentType(); int getContentLength(); String getCharacterEncoding();
 java.io.BufferedReader getReader() throws java.io.IOException; javax.servlet.ServletInputStream getInputStream() throws java.io.IOException;
 HttpSession getSession(); HttpSession getSession(boolean c); Object getAttribute(String n); void setAttribute(String n, Object o); java.util.Locale getLocale();
 Part getPart(String n) throws java.io.IOException, javax.servlet.ServletException; Collection<Part> getParts() throws java.io.IOException, javax.servlet.ServletException; }
