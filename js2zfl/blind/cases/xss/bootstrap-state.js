const express = require('express');

const app = express();

app.get('/app', (req, res) => {
  const initial = {
    locale: req.query.locale || 'en',
    returnTo: req.query.returnTo || '/',
  };
  res.send(`<!doctype html>
<html>
  <body>
    <div id="root"></div>
    <script>window.__INITIAL_STATE__ = ${JSON.stringify(initial)};</script>
    <script src="/bundle.js"></script>
  </body>
</html>`);
});

module.exports = app;
