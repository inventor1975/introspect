const express = require('express');
const { execFile } = require('child_process');

const app = express();

app.get('/domains/whois', (req, res) => {
  const domain = String(req.query.domain || '').trim();
  if (!domain) return res.status(400).send('domain required');
  execFile('whois', [domain], { timeout: 8000 }, (err, stdout) => {
    if (err) return res.status(504).send('lookup failed');
    res.type('text/plain').send(stdout);
  });
});

module.exports = app;
