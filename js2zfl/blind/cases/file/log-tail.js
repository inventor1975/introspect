'use strict';
const express = require('express');
const fs = require('fs');
const path = require('path');

const LOG_DIR = process.env.LOG_DIR || '/var/log/myapp';
const app = express();

function requireAdmin(req, res, next) {
  if (req.get('x-admin-token') !== process.env.ADMIN_TOKEN) return res.sendStatus(401);
  next();
}

app.get('/admin/logs', requireAdmin, (req, res) => {
  const file = path.normalize(req.query.file || 'app.log');
  if (file.startsWith('..')) {
    return res.status(400).send('invalid log file');
  }
  const full = path.resolve(LOG_DIR, file);
  const lines = Math.min(parseInt(req.query.lines, 10) || 200, 2000);
  fs.readFile(full, 'utf8', (err, text) => {
    if (err) return res.status(404).json({ error: 'not found' });
    res.type('text/plain').send(text.split('\n').slice(-lines).join('\n'));
  });
});

module.exports = app;
