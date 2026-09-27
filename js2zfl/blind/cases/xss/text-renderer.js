const express = require('express');
const escapeHtml = require('escape-html');

const app = express();

const renderers = {
  plain: (s) => escapeHtml(s),
  code: (s) => `<pre><code>${escapeHtml(s)}</code></pre>`,
  html: (s) => s,
};

app.get('/render', (req, res) => {
  const mode = req.query.mode in renderers ? req.query.mode : 'plain';
  const render = renderers[mode];
  res.send(`<div class="rendered">${render(String(req.query.text || ''))}</div>`);
});

module.exports = app;
