const express = require('express');
const fs = require('fs');
const path = require('path');

const router = express.Router();
const MEDIA_ROOT = path.resolve(__dirname, '../media');

router.get('/media/raw', (req, res) => {
  const file = req.query.file;
  if (typeof file !== 'string' || file.includes('..')) {
    return res.status(400).json({ error: 'invalid file' });
  }
  const location = path.resolve(MEDIA_ROOT, file);
  fs.stat(location, (err, info) => {
    if (err || !info.isFile()) {
      return res.sendStatus(404);
    }
    res.setHeader('Content-Length', info.size);
    fs.createReadStream(location).pipe(res);
  });
});

module.exports = router;
