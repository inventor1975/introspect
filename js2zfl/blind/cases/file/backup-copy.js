const express = require('express');
const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, 'data', 'app.sqlite');
const BACKUP = path.join(__dirname, 'backups');
const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/maintenance/backup', (req, res) => {
  const target = req.body.target || `backup-${new Date().toISOString().slice(0, 10)}.sqlite`;
  const dest = path.join(BACKUP, target);
  fs.copyFile(DB_FILE, dest, (err) => {
    if (err) return res.status(500).json({ error: 'backup failed' });
    res.json({ backup: target });
  });
});

module.exports = app;
