const express = require('express');

const app = express();

app.get('/results', (req, res) => {
  const q = String(req.query.q || '');
  const page = Math.max(1, parseInt(req.query.page, 10) || 1);
  const href = `/results?q=${encodeURIComponent(q)}&amp;page=${page + 1}`;
  res.send(`<nav><a class="next" href="${href}">Next page (${page + 1})</a></nav>`);
});

module.exports = app;
