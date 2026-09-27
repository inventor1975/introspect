const express = require('express');
const escapeHtml = require('escape-html');
const fs = require('fs');
const path = require('path');

const NOTES = path.join(__dirname, 'notes');
const app = express();

app.get('/notes/open', (req, res) => {
  const name = escapeHtml(req.query.name || '');
  if (!name) return res.status(400).send('missing note name');
  fs.readFile(path.join(NOTES, name), 'utf8', (err, text) => {
    if (err) return res.status(404).send('note ' + name + ' not found');
    res.json({ name, text });
  });
});

module.exports = app;
