const express = require('express');

const app = express();

const SORT_OPTIONS = ['newest', 'oldest', 'popular', 'price'];

app.get('/listings', (req, res) => {
  const sort = req.query.sort || 'newest';
  if (!SORT_OPTIONS.includes(sort)) {
    return res.status(400).send('<p>Unknown sort order.</p>');
  }
  res.send(`<div class="toolbar">Sorted by <strong>${sort}</strong></div><div id="list"></div>`);
});

module.exports = app;
