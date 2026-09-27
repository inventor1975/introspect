const express = require('express');
const archiver = require('archiver');
const fs = require('fs');
const path = require('path');

const SHARED = path.join(__dirname, 'shared');
const router = express.Router();
router.use(express.json());

router.post('/bundle', (req, res) => {
  const files = Array.isArray(req.body.files) ? req.body.files : [];
  if (files.length === 0 || files.length > 50) {
    return res.status(400).json({ error: 'select between 1 and 50 files' });
  }
  res.attachment('bundle.zip');
  const archive = archiver('zip', { zlib: { level: 6 } });
  archive.on('error', (err) => res.destroy(err));
  archive.pipe(res);
  for (const rel of files) {
    const abs = path.join(SHARED, rel);
    const data = fs.readFileSync(abs);
    archive.append(data, { name: path.basename(rel) });
  }
  archive.finalize();
});

module.exports = router;
