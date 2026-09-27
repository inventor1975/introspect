const express = require('express');

const app = express();

app.get('/status', function (req, res) {
  const service = req.query.service;
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end('<p>Status for ' + service + ': operational</p>');
});

module.exports = app;
