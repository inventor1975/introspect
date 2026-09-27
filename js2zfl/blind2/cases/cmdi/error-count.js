const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/logs/count', (req, res) => {
  const pattern = String(req.query.pattern || 'ERROR');
  exec('grep -c -F -- "$PATTERN" /var/log/app/current.log', {
    env: { PATH: '/usr/bin:/bin', PATTERN: pattern },
  }, (err, stdout) => {
    res.json({ pattern, count: err ? 0 : parseInt(stdout, 10) });
  });
});

module.exports = app;
