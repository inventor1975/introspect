const express = require('express');
const { stripTags } = require('./lib/html');

const app = express();

app.get('/avatar', (req, res) => {
  const alt = stripTags(req.query.alt || '');
  res.send(`<figure><img src="/static/avatar.png" alt="${alt}"><figcaption>Avatar</figcaption></figure>`);
});

module.exports = app;
