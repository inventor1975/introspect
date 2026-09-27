const express = require('express');
const { escapeHtml } = require('./lib/html');

const app = express();

app.get('/out', (req, res) => {
  let target;
  try {
    target = new URL(String(req.query.url || ''));
  } catch (err) {
    return res.status(400).send('<p>Invalid link.</p>');
  }
  if (target.protocol !== 'https:' && target.protocol !== 'http:') {
    return res.status(400).send('<p>Only web links can be followed.</p>');
  }
  res.send(
    `<p>You are leaving the site.</p><a rel="noopener" href="${escapeHtml(target.href)}">Continue to ${escapeHtml(target.hostname)}</a>`
  );
});

module.exports = app;
