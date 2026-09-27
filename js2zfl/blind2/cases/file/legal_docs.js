const express = require('express');
const path = require('path');

const LEGAL_DIR = path.join(__dirname, 'legal');
const PUBLISHED = new Set(['terms.pdf', 'privacy.pdf', 'cookies.pdf', 'dpa.pdf']);

const app = express();

app.get('/legal/:doc', (req, res) => {
  const doc = req.params.doc;
  if (!PUBLISHED.has(doc)) {
    return res.status(404).send(`Unknown document`);
  }
  res.download(path.join(LEGAL_DIR, doc));
});

module.exports = app;
