const express = require('express');
const escapeHtml = require('escape-html');

const app = express();

const formatters = new Map([
  ['plain', (s) => escapeHtml(s)],
  ['quote', (s) => `<blockquote>${escapeHtml(s)}</blockquote>`],
  ['code', (s) => `<pre><code>${escapeHtml(s)}</code></pre>`],
]);

app.get('/snippet', (req, res) => {
  const format = formatters.get(req.query.style) || formatters.get('plain');
  res.send(`<div class="snippet">${format(String(req.query.text || ''))}</div>`);
});

module.exports = app;
