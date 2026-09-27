const express = require('express');
const multer = require('multer');
const sanitize = require('sanitize-filename');
const fs = require('fs');
const path = require('path');

const ATTACHMENTS = path.join(__dirname, 'attachments');
const upload = multer({ storage: multer.memoryStorage() });
const router = express.Router();

router.post('/messages/:messageId/attachments', upload.single('file'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'file required' });
  const safeName = sanitize(req.body.name || req.file.originalname);
  if (!safeName) return res.status(400).json({ error: 'invalid file name' });
  const dir = path.join(ATTACHMENTS, String(Number(req.params.messageId) || 0));
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, safeName), req.file.buffer);
  res.status(201).json({ name: safeName });
});

module.exports = router;
