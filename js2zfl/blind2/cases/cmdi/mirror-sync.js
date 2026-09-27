const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

const settings = {
  mirrorSource: 'rsync://mirror.internal/pub/',
};

app.put('/admin/mirror', (req, res) => {
  if (req.body.source) {
    settings.mirrorSource = req.body.source;
  }
  res.json(settings);
});

app.post('/admin/mirror/sync', (req, res) => {
  exec(`rsync -az --delete ${settings.mirrorSource} /srv/mirror/`, (err) => {
    res.json({ synced: !err });
  });
});

module.exports = app;
