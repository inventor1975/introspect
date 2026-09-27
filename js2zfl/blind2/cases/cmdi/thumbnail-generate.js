const express = require('express');
const { execFile } = require('child_process');
const path = require('path');

const router = express.Router();
const MEDIA_ROOT = '/srv/media';
const NAME_RE = /^[A-Za-z0-9_]+\.(png|jpe?g)$/;
const SIZES = { small: '120x120', medium: '320x320', large: '640x640' };

router.get('/thumbnails', (req, res) => {
  const src = req.query.src;
  const size = SIZES[req.query.size] ? SIZES[req.query.size] : SIZES.small;
  if (typeof src !== 'string' || !NAME_RE.test(src)) {
    return res.status(400).json({ error: 'invalid source' });
  }
  const out = path.join(MEDIA_ROOT, 'thumbs', src);
  execFile('convert', [path.join(MEDIA_ROOT, src), '-resize', size, out], (err) => {
    if (err) return res.status(500).json({ error: 'conversion failed' });
    res.sendFile(out);
  });
});

module.exports = router;
