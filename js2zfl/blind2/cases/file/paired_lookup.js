const express = require('express');
const fs = require('fs');
const path = require('path');

const router = express.Router();
const CATALOG_BASE = path.join(__dirname, 'catalog');

router.get('/catalog/item', (req, res) => {
  const { section = 'general', item } = req.query;
  if (!item) {
    return res.status(400).json({ error: 'item is required' });
  }
  const itemPath = path.join(CATALOG_BASE, section, `${item}.json`);
  let record;
  try {
    record = JSON.parse(fs.readFileSync(itemPath, 'utf8'));
  } catch (e) {
    return res.status(404).json({ error: 'unknown item' });
  }
  res.json(record);
});

module.exports = router;
