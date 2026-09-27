const express = require('express');
const escapeHtml = require('escape-html');

const app = express();

app.get('/recipes/shopping-list', (req, res) => {
  const items = String(req.query.items || '').split(',');
  res.type('html');
  res.write('<ol class="shopping">');
  for (let i = 0; i < items.length; i++) {
    const item = escapeHtml(items[i].trim());
    if (!item) continue;
    res.write(`<li>${item}</li>`);
  }
  res.end('</ol>');
});

module.exports = app;
