'use strict';

const express = require('express');
const multer = require('multer');
const { execFile } = require('child_process');

const upload = multer({ dest: '/srv/tmp/uploads', limits: { fileSize: 20 * 1024 * 1024 } });
const app = express();

app.post('/pdf/extract', upload.single('document'), (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'no file' });
  const original = req.file.originalname;
  execFile('pdftotext', ['-layout', req.file.path, '-'], { maxBuffer: 16 << 20 }, (err, stdout) => {
    if (err) return res.status(422).json({ error: `could not read ${original}` });
    res.json({ name: original, text: stdout });
  });
});

module.exports = app;
