const express = require('express');
const multer = require('multer');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const db = require('./lib/db');

const STORE = path.join(__dirname, 'blobstore');
const upload = multer({ storage: multer.memoryStorage() });
const router = express.Router();

router.post('/files', upload.single('file'), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'file required' });
  const record = {
    id: crypto.randomUUID(),
    storageKey: crypto.randomBytes(16).toString('hex'),
    originalName: req.file.originalname,
    mime: req.file.mimetype,
  };
  await fs.promises.writeFile(path.join(STORE, record.storageKey), req.file.buffer);
  await db.insertUpload(record);
  res.status(201).json({ id: record.id });
});

router.get('/files/:id', async (req, res) => {
  const doc = await db.findUpload(req.params.id);
  if (!doc) return res.sendStatus(404);
  res.type(doc.mime);
  res.sendFile(path.join(STORE, doc.storageKey));
});

module.exports = router;
