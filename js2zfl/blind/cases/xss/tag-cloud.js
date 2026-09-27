const express = require('express');

const app = express();

app.get('/tags', (req, res) => {
  const raw = String(req.query.tags || '');
  const tags = raw.split(',').map((t) => t.trim()).filter(Boolean);

  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  res.write('<ul class="tags">');
  for (const tag of tags) {
    res.write('<li>' + tag + '</li>');
  }
  res.end('</ul>');
});

module.exports = app;
