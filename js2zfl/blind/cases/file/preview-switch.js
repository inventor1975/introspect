const express = require('express');
const path = require('path');

const PREVIEW = path.join(__dirname, 'renders', 'preview');
const FULL = path.join(__dirname, 'renders', 'full');
const router = express.Router();

router.get('/render', (req, res) => {
  const wantsPreview = req.query.preview === '1';
  const target = wantsPreview
    ? path.join(PREVIEW, req.query.file || 'blank.png')
    : path.join(FULL, 'default.pdf');
  res.sendFile(target, (err) => {
    if (err) res.status(404).json({ error: 'render missing' });
  });
});

module.exports = router;
