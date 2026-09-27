const express = require('express');
const fs = require('fs/promises');
const path = require('path');
const { escapeHtml } = require('./lib/html');

const router = express.Router();
const NOTES_DIR = path.join(__dirname, 'notes');

router.get('/notes/view', async (req, res) => {
  const noteName = escapeHtml(req.query.name || 'index.txt');
  let content;
  try {
    content = await fs.readFile(path.join(NOTES_DIR, noteName), 'utf8');
  } catch (err) {
    return res.status(404).send(`<p>No note called ${noteName}</p>`);
  }
  res.send(`<h1>${noteName}</h1><pre>${escapeHtml(content)}</pre>`);
});

module.exports = router;
