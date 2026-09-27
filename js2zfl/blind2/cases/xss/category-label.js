const express = require('express');

const app = express();

const LABELS = Object.freeze({
  books: 'Books &amp; Magazines',
  garden: 'Garden',
  toys: 'Toys',
});

app.get('/category', (req, res) => {
  const key = req.query.c;
  const label = Object.prototype.hasOwnProperty.call(LABELS, key) ? LABELS[key] : 'All products';
  res.send(`<h2 class="category">${label}</h2>`);
});

module.exports = app;
