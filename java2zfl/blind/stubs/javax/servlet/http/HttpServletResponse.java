package javax.servlet.http; public interface HttpServletResponse {
 int SC_OK=200; int SC_BAD_REQUEST=400; int SC_FORBIDDEN=403; int SC_NOT_FOUND=404; int SC_INTERNAL_SERVER_ERROR=500;
 java.io.PrintWriter getWriter() throws java.io.IOException; javax.servlet.ServletOutputStream getOutputStream() throws java.io.IOException;
 void setContentType(String t); void setCharacterEncoding(String e); void setHeader(String n, String v); void addHeader(String n, String v); void addCookie(Cookie c);
 void setStatus(int s); void sendError(int s) throws java.io.IOException; void sendError(int s, String m) throws java.io.IOException; void sendRedirect(String l) throws java.io.IOException; }
