const express = require('express');
const escapeHtml = require('escape-html');
const banner = require('./config/banner.json');

const app = express();

app.get('/home', (req, res) => {
  const top = banner.enabled ? banner.html : '';
  const who = escapeHtml(req.query.who || 'there');
  res.send(`${top}<h1>Hi ${who}</h1>`);
});

module.exports = app;
