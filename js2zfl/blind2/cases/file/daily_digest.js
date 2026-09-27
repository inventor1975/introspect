const express = require('express');
const fs = require('fs');
const path = require('path');

const DIGEST_DIR = path.join(__dirname, 'digests');
const router = express.Router();

router.get('/digest', (req, res) => {
  const requested = new Date(req.query.date || Date.now());
  if (Number.isNaN(requested.getTime())) {
    return res.status(400).json({ error: `bad date ${req.query.date}` });
  }
  const day = requested.toISOString().slice(0, 10);
  const file = path.join(DIGEST_DIR, `digest-${day}.html`);
  fs.readFile(file, 'utf8', (err, html) => {
    if (err) return res.status(404).send('No digest for that day');
    res.type('html').send(html);
  });
});

module.exports = router;
