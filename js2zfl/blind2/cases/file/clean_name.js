const express = require('express');
const sanitize = require('sanitize-filename');
const fs = require('fs');
const path = require('path');

const INBOX = path.join(__dirname, 'inbox');
const app = express();

app.post('/inbox', express.raw({ type: '*/*', limit: '5mb' }), (req, res) => {
  const supplied = req.get('X-Filename') || '';
  const fileName = sanitize(supplied);
  if (!fileName) {
    return res.status(400).json({ error: 'filename rejected' });
  }
  fs.writeFile(path.join(INBOX, fileName), req.body, (err) => {
    if (err) return res.status(500).end();
    res.status(201).json({ stored: fileName });
  });
});

module.exports = app;
