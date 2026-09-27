const express = require('express');

const app = express();

app.get('/app', (req, res) => {
  const initialState = {
    route: req.path,
    filter: req.query.filter || 'all',
    user: null,
  };
  res.send(`<!doctype html>
<html>
  <body>
    <div id="root"></div>
    <script>window.__INITIAL_STATE__ = ${JSON.stringify(initialState)};</script>
    <script src="/bundle.js"></script>
  </body>
</html>`);
});

module.exports = app;
