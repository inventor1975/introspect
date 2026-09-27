const express = require('express');

const app = express();

app.get('/search', (req, res) => {
  const term = req.query.q || '';
  res.send('<h1>Results for ' + term + '</h1><p>No matches found.</p>');
});

module.exports = app;
