const express = require('express');

const app = express();

function serializeState(state) {
  return JSON.stringify(state)
    .replace(/</g, '\\u003c')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

app.get('/workspace', (req, res) => {
  const initialState = {
    route: req.path,
    filter: req.query.filter || 'all',
    search: req.query.search || '',
  };
  res.send(`<!doctype html>
<html>
  <body>
    <div id="root"></div>
    <script>window.__INITIAL_STATE__ = ${serializeState(initialState)};</script>
    <script src="/bundle.js"></script>
  </body>
</html>`);
});

module.exports = app;
