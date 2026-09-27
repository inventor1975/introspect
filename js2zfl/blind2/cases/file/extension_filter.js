const express = require('express');
const fs = require('fs');
const path = require('path');

const ALLOWED_EXTENSIONS = ['.json', '.yaml', '.yml'];
const SETTINGS_DIR = path.join(__dirname, 'settings');

const app = express();

app.get('/settings/raw', (req, res) => {
  const name = req.query.name;
  if (typeof name !== 'string') {
    return res.status(400).end();
  }
  const ext = path.extname(name).toLowerCase();
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return res.status(415).json({ error: `extension ${ext} not allowed` });
  }
  fs.promises
    .readFile(path.join(SETTINGS_DIR, name), 'utf8')
    .then((text) => res.type('text/plain').send(text))
    .catch(() => res.sendStatus(404));
});

module.exports = app;
