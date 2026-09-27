const express = require('express');
const multer = require('multer');
const AdmZip = require('adm-zip');
const fs = require('fs');
const path = require('path');

const PLUGIN_DIR = path.join(__dirname, 'plugins');
const upload = multer({ storage: multer.memoryStorage() });
const router = express.Router();

router.post('/admin/plugins', upload.single('bundle'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'bundle required' });
  const zip = new AdmZip(req.file.buffer);
  const slug = path.basename(req.file.originalname, '.zip');
  const dest = path.join(PLUGIN_DIR, slug);
  const written = [];
  for (const entry of zip.getEntries()) {
    if (entry.isDirectory) continue;
    const out = path.join(dest, entry.entryName);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, entry.getData());
    written.push(entry.entryName);
  }
  res.status(201).json({ plugin: slug, files: written.length });
});

module.exports = router;
