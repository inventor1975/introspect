const express = require('express');
const { escapeHtml } = require('./lib/html');

const app = express();

app.get('/cart/edit', (req, res) => {
  const qty = escapeHtml(req.query.qty || '1');
  res.send(
    '<form method="post" action="/cart"><input name=qty value=' + qty + '><button>Update</button></form>'
  );
});

module.exports = app;
