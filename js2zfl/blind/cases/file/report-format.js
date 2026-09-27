const express = require('express');
const fs = require('fs');
const path = require('path');

const REPORT_DIR = path.join(__dirname, 'generated');
const app = express();

app.get('/reports/latest', (req, res) => {
  const fmt = req.query.format;
  let file;
  switch (fmt) {
    case 'csv':
      file = 'latest.csv';
      break;
    case 'xlsx':
      file = 'latest.xlsx';
      break;
    default:
      file = 'latest.json';
  }
  const full = path.join(REPORT_DIR, file);
  if (!fs.existsSync(full)) return res.status(404).json({ error: `no ${fmt || 'json'} report yet` });
  res.download(full);
});

module.exports = app;
