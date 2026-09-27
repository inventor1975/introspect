'use strict';

const express = require('express');
const fs = require('fs');
const path = require('path');

const INDEX_FILE = path.join(__dirname, 'data', 'search-index.txt');
const router = express.Router();

router.get('/search', (req, res) => {
  const term = String(req.query.q || '').toLowerCase();
  const indexName = req.query.index || 'default';
  fs.readFile(INDEX_FILE, 'utf8', (err, text) => {
    if (err) return res.status(503).json({ error: 'index unavailable' });
    const hits = text
      .split('\n')
      .filter((line) => line.toLowerCase().includes(term))
      .slice(0, 50);
    res.json({ index: indexName, hits });
  });
});

module.exports = router;
