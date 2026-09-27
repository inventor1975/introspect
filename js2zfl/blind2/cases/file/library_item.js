const express = require('express');
const path = require('path');

const IMAGE_DIR = '/srv/library/images';
const DOC_DIR = '/srv/library/documents';
const KINDS = ['image', 'document'];

const app = express();

app.get('/library/item', (req, res) => {
  const kind = req.query.kind;
  if (!KINDS.includes(kind)) {
    return res.status(400).send('unknown kind');
  }
  let dir;
  if (kind === 'image') {
    dir = IMAGE_DIR;
  } else {
    dir = DOC_DIR;
  }
  const fileName = req.query.name;
  res.sendFile(path.join(dir, fileName));
});

module.exports = app;
