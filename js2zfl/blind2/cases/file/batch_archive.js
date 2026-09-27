const express = require('express');
const fs = require('fs');
const path = require('path');

const ACTIVE = path.join(__dirname, 'records', 'active');
const ARCHIVE = path.join(__dirname, 'records', 'archive');

const router = express.Router();

router.post('/records/archive', express.json(), async (req, res) => {
  const ids = Array.isArray(req.body.ids) ? req.body.ids : [];
  const moved = [];
  const skipped = [];
  for (const raw of ids) {
    const id = Number(raw);
    if (!Number.isSafeInteger(id) || id < 1) {
      skipped.push(raw);
      continue;
    }
    const name = `record-${id}.json`;
    try {
      await fs.promises.rename(path.join(ACTIVE, name), path.join(ARCHIVE, name));
      moved.push(id);
    } catch (err) {
      skipped.push(raw);
    }
  }
  res.json({ moved, skipped });
});

module.exports = router;
