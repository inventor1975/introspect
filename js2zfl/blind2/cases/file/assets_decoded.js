const express = require('express');
const fs = require('fs');
const path = require('path');

const ASSET_ROOT = path.join(__dirname, 'static');
const router = express.Router();

router.get('/assets/*', (req, res) => {
  const raw = req.path.slice('/assets/'.length);
  if (raw.includes('..')) {
    return res.status(400).send('bad path');
  }
  const relative = decodeURIComponent(raw);
  const location = path.join(ASSET_ROOT, relative);
  fs.readFile(location, (err, buf) => {
    if (err) return res.sendStatus(404);
    res.type(path.extname(location)).send(buf);
  });
});

module.exports = router;
