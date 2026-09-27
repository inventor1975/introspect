const { format } = require('util');
const express = require('express');

const app = express();

app.get('/downloads', (req, res) => {
  const count = req.query.count;
  const html = format('<span class="downloads">%d downloads this week</span>', count);
  res.send(html);
});

module.exports = app;
