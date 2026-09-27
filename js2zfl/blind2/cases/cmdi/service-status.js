const express = require('express');
const { exec } = require('child_process');

const app = express();
const UNIT_PATTERN = /[a-z0-9-]+\.service/;

app.get('/services/status', (req, res) => {
  const unit = req.query.unit;
  if (!UNIT_PATTERN.test(unit)) {
    return res.status(400).json({ error: 'invalid unit name' });
  }
  exec(`systemctl status ${unit} --no-pager`, (err, stdout) => {
    res.json({ unit, active: !err, detail: stdout });
  });
});

module.exports = app;
