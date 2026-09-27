const express = require('express');
const fs = require('fs');
const path = require('path');

const SNIPPETS = path.join(__dirname, 'snippets');
const app = express();
app.use(express.json());

function toFileStem(label) {
  return String(label).replace(/[^a-zA-Z0-9_-]/g, '').slice(0, 80) || 'untitled';
}

app.post('/snippets', (req, res) => {
  const stem = toFileStem(req.body.label);
  const destination = path.join(SNIPPETS, stem + '.txt');
  fs.writeFile(destination, String(req.body.text || ''), { flag: 'w' }, (err) => {
    if (err) return res.status(500).json({ error: 'write failed' });
    res.status(201).json({ saved: stem });
  });
});

module.exports = app;
