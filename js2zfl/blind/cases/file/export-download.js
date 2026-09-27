const express = require('express');
const path = require('path');
const fs = require('fs');

const BASE = path.resolve('/var/lib/exports');
const router = express.Router();

router.get('/exports/download', (req, res) => {
  const requested = String(req.query.name || '');
  const resolved = path.resolve(BASE, requested);
  if (!resolved.startsWith(BASE + path.sep)) {
    return res.status(403).json({ error: 'forbidden' });
  }
  const stream = fs.createReadStream(resolved);
  stream.on('error', () => res.status(404).end());
  res.setHeader('Content-Type', 'text/csv');
  stream.pipe(res);
});

module.exports = router;
