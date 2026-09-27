<%@ page contentType="text/html;charset=UTF-8" %>
<html>
<head><title>Account</title></head>
<body>
  <h1>Welcome back, ${nickname}</h1>
  <div class="tabs" data-active="${tab}">
    <a href="?tab=overview">Overview</a>
    <a href="?tab=billing">Billing</a>
  </div>
</body>
</html>
