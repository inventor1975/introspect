const express = require('express');
const { escapeHtml } = require('./lib/html');

const app = express();

app.get('/suggest', (req, res) => {
  const q = String(req.query.q || '');
  const shown = escapeHtml(q).slice(0, 60);
  res.send(`<p>Did you mean <strong>${shown}</strong>${q.length > 60 ? '&hellip;' : ''}?</p>`);
});

module.exports = app;
