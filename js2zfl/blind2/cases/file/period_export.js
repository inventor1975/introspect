const express = require('express');
const fs = require('fs');
const path = require('path');

const EXPORTS = path.join(__dirname, 'exports');
const app = express();

app.get('/analytics/export', (req, res) => {
  const period = req.query.period;
  let target;
  if (period === 'week') {
    target = 'weekly-summary.csv';
  } else if (period === 'month') {
    target = 'monthly-summary.csv';
  } else {
    target = 'daily-summary.csv';
  }
  res.attachment(`${period || 'daily'}.csv`);
  fs.createReadStream(path.join(EXPORTS, target)).pipe(res);
});

module.exports = app;
