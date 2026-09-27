package javax.servlet.http; public interface Part { String getName(); String getSubmittedFileName(); java.io.InputStream getInputStream() throws java.io.IOException; long getSize(); }
