const express = require('express');
const AdmZip = require('adm-zip');
const fs = require('fs');
const path = require('path');

const THEME_DIR = path.join(__dirname, 'themes');
const router = express.Router();

router.post('/themes/import', express.raw({ type: 'application/zip', limit: '25mb' }), (req, res) => {
  let zip;
  try {
    zip = new AdmZip(req.body);
  } catch (err) {
    return res.status(400).json({ error: 'not a zip archive' });
  }
  const written = [];
  for (const entry of zip.getEntries()) {
    if (entry.isDirectory) continue;
    const destination = path.join(THEME_DIR, entry.entryName);
    fs.mkdirSync(path.dirname(destination), { recursive: true });
    fs.writeFileSync(destination, entry.getData());
    written.push(entry.entryName);
  }
  res.json({ imported: written.length });
});

module.exports = router;
