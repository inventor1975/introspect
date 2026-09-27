const express = require('express');
const path = require('path');

const QUARTERLY = path.join(__dirname, 'reports', 'quarterly-report.pdf');
const app = express();

app.get('/reports/quarterly', (req, res) => {
  const saveAs = req.query.saveAs || 'quarterly-report.pdf';
  res.download(QUARTERLY, saveAs, (err) => {
    if (err && !res.headersSent) res.status(500).send('download failed');
  });
});

module.exports = app;
