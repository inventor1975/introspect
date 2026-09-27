const express = require('express');
const archiver = require('archiver');
const fs = require('fs');
const path = require('path');

const PRESS_KIT = path.join(__dirname, 'press-kit');
const AVAILABLE = new Set(['logo.svg', 'logo-dark.svg', 'wordmark.png', 'founders.jpg', 'fact-sheet.pdf']);
const router = express.Router();
router.use(express.json());

router.post('/press-kit/bundle', (req, res) => {
  const requested = Array.isArray(req.body.files) ? req.body.files : [];
  const selected = requested.filter((f) => AVAILABLE.has(f));
  if (selected.length === 0) return res.status(400).json({ error: 'nothing selected' });
  res.attachment('press-kit.zip');
  const archive = archiver('zip');
  archive.pipe(res);
  for (const name of selected) {
    archive.append(fs.readFileSync(path.join(PRESS_KIT, name)), { name });
  }
  archive.finalize();
});

module.exports = router;
