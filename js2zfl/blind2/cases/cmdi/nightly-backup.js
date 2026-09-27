const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');

const config = JSON.parse(fs.readFileSync('/etc/app/backup.json', 'utf8'));

const app = express();

app.post('/admin/backup/run', (req, res) => {
  const label = req.query.label || 'manual';
  exec(config.backupCommand, { env: { ...process.env, BACKUP_TARGET: config.target } }, (err) => {
    res.json({ label, ok: !err });
  });
});

module.exports = app;
