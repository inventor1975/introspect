<%@ page contentType="text/html;charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
<head><title>Order history</title></head>
<body>
  <h1>Your orders</h1>
  <c:if test="${not empty filter}">
    <p>Filtered by: <strong><c:out value="${filter}"/></strong></p>
  </c:if>
  <table id="orders"></table>
</body>
</html>
