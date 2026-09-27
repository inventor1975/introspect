const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/status', (req, res) => {
  const requester = req.query.who || req.get('user-agent');
  exec('uptime -p', (err, stdout) => {
    res.json({
      requestedBy: requester,
      uptime: err ? null : stdout.trim(),
    });
  });
});

module.exports = app;
