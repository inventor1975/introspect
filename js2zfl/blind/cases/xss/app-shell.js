const express = require('express');

const app = express();

function serializeForScript(value) {
  return JSON.stringify(value)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/&/g, '\\u0026');
}

app.get('/shell', (req, res) => {
  const bootstrap = {
    route: req.query.route || '/',
    campaign: req.query.utm_campaign || null,
  };
  res.send(`<!doctype html>
<html>
  <body>
    <div id="app"></div>
    <script>window.__BOOT__ = ${serializeForScript(bootstrap)};</script>
    <script src="/static/shell.js"></script>
  </body>
</html>`);
});

module.exports = app;
