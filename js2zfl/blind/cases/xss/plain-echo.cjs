'use strict';

const express = require('express');

const app = express();

app.get('/echo', (req, res) => {
  const message = req.query.message || '';
  res.type('text/plain').send('<echo> ' + message);
});

module.exports = app;
