const crypto = require('crypto');
const express = require('express');

const app = express();

app.get('/avatar', (req, res) => {
  const email = String(req.query.email || '').trim().toLowerCase();
  const hash = crypto.createHash('md5').update(email).digest('hex');
  const size = Math.min(Math.max(parseInt(req.query.s, 10) || 80, 16), 512);
  res.send(`<img alt="avatar" width="${size}" height="${size}" src="https://www.gravatar.com/avatar/${hash}?s=${size}&d=identicon">`);
});

module.exports = app;
