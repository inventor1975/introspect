const express = require('express');
const fs = require('fs');
const path = require('path');

const ARCHIVE = path.join(__dirname, 'archive');
const app = express();

app.get('/archive/entry', (req, res) => {
  const raw = req.query.p;
  if (typeof raw !== 'string' || raw.includes('..')) {
    return res.status(400).json({ error: 'bad path' });
  }
  let rel;
  try {
    rel = decodeURIComponent(raw);
  } catch (e) {
    return res.status(400).json({ error: 'bad encoding' });
  }
  fs.readFile(path.join(ARCHIVE, rel), (err, data) => {
    if (err) return res.sendStatus(404);
    res.type('application/octet-stream').send(data);
  });
});

module.exports = app;
