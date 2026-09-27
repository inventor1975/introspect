const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const SHARE_ROOT = '/srv/fileshare';

app.get('/share', (req, res) => {
  const rel = String(req.query.path || '');
  if (!rel.startsWith('public/')) {
    return res.status(403).json({ error: 'only public files can be shared' });
  }
  const stream = fs.createReadStream(path.join(SHARE_ROOT, rel));
  stream.on('error', () => res.status(404).end());
  res.attachment(path.basename(rel));
  stream.pipe(res);
});

module.exports = app;
