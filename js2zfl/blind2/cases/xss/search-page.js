const express = require('express');
const { escapeHtml } = require('./lib/html');

const app = express();

app.get('/find', (req, res) => {
  const term = req.query.q || '';
  res.send('<h1>Results for ' + escapeHtml(term) + '</h1><p>No matches found.</p>');
});

module.exports = app;
