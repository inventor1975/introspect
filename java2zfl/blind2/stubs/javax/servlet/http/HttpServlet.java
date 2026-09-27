package javax.servlet.http; public abstract class HttpServlet {
 public void init() throws javax.servlet.ServletException {} public javax.servlet.ServletConfig getServletConfig(){return null;} public String getInitParameter(String n){return null;}
 protected void doGet(HttpServletRequest q, HttpServletResponse s) throws javax.servlet.ServletException, java.io.IOException {}
 protected void doPost(HttpServletRequest q, HttpServletResponse s) throws javax.servlet.ServletException, java.io.IOException {}
 protected void doPut(HttpServletRequest q, HttpServletResponse s) throws javax.servlet.ServletException, java.io.IOException {}
 protected void doDelete(HttpServletRequest q, HttpServletResponse s) throws javax.servlet.ServletException, java.io.IOException {} }
