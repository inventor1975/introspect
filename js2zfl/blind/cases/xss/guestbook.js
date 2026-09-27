const express = require('express');
const xss = require('xss');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/guestbook/preview', (req, res) => {
  const name = xss(req.body.name || 'Visitor');
  const message = xss(req.body.message || '');
  res.send('<div class="entry"><b>' + name + '</b> wrote:<p>' + message + '</p></div>');
});

module.exports = app;
