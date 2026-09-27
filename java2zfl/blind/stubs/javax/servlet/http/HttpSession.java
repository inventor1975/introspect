package javax.servlet.http; public interface HttpSession { Object getAttribute(String n); void setAttribute(String n, Object v); void removeAttribute(String n); String getId(); void invalidate(); }
