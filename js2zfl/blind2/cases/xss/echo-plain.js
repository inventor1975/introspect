const express = require('express');

const app = express();

app.get('/debug/echo', (req, res) => {
  const message = req.query.m || '';
  res.set('X-Content-Type-Options', 'nosniff');
  res.type('text/plain');
  res.send('You said: ' + message);
});

module.exports = app;
