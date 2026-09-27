const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/logs/head', (req, res) => {
  const n = parseInt(req.query.n, 10);
  if (Number.isNaN(n) || n <= 0) {
    return res.status(400).send(`invalid line count: ${req.query.n}`);
  }
  exec(`head -n ${n} /var/log/app/current.log`, (err, stdout) => {
    if (err) return res.sendStatus(500);
    res.type('text').send(stdout);
  });
});

module.exports = app;
