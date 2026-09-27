const express = require('express');
const { exec } = require('child_process');
const path = require('path');

const router = express.Router();
const MEDIA_ROOT = '/srv/media';

router.get('/thumbs', (req, res) => {
  const src = req.query.src;
  const size = req.query.size || '200x200';
  const out = path.join(MEDIA_ROOT, 'thumbs', `${Date.now()}.jpg`);
  exec(`convert ${MEDIA_ROOT}/${src} -resize ${size} ${out}`, (err) => {
    if (err) {
      return res.status(500).json({ error: 'conversion failed' });
    }
    res.sendFile(out);
  });
});

module.exports = router;
