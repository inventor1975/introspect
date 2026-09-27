const express = require('express');
const util = require('util');
const { exec } = require('child_process');

const app = express();

app.get('/whois', (req, res) => {
  const command = util.format('whois %s | head -n 40', req.query.domain);
  exec(command, { timeout: 8000 }, (err, stdout) => {
    if (err) return res.status(504).send('lookup failed');
    res.type('text/plain').send(stdout);
  });
});

module.exports = app;
