const express = require('express');

const app = express();

const ALLOWED_TAGS = new Set(['news', 'events', 'jobs', 'sports']);

app.get('/feed/tags', (req, res) => {
  const tags = String(req.query.tags || '')
    .split(',')
    .map((t) => t.trim().toLowerCase())
    .filter((t) => ALLOWED_TAGS.has(t));

  let html = '<ul class="tags">';
  for (const tag of tags) {
    html += `<li><a href="/feed?tag=${tag}">${tag}</a></li>`;
  }
  html += '</ul>';
  res.send(html);
});

module.exports = app;
