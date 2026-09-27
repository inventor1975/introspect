const express = require('express');
const formatters = require('./lib/formatters');

const app = express();

app.get('/format', (req, res) => {
  const style = req.query.style || 'plain';
  const format = formatters[style];
  if (typeof format !== 'function') {
    return res.status(400).send('<p>Unsupported style.</p>');
  }
  res.send('<div class="formatted">' + format(req.query.value || '') + '</div>');
});

module.exports = app;
