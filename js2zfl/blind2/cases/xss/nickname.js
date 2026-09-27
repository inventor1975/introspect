const express = require('express');

const app = express();

app.get('/nick', (req, res) => {
  let nick = String(req.query.nick || '');
  nick = nick.replace('<', '&lt;').replace('>', '&gt;');
  res.send('<span class="nick">' + nick + '</span>');
});

module.exports = app;
