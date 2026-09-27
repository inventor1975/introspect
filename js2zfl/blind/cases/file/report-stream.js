const express = require('express');
const fs = require('fs');
const path = require('path');

const DIR = path.join(__dirname, 'reports');
const REPORTS = new Map([
  ['daily', path.join(DIR, 'daily-summary.csv')],
  ['weekly', path.join(DIR, 'weekly-summary.csv')],
  ['churn', path.join(DIR, 'churn.csv')],
]);

const router = express.Router();

router.get('/reports/:kind.csv', (req, res) => {
  const file = REPORTS.get(req.params.kind);
  if (!file) return res.status(404).json({ error: 'unknown report' });
  res.type('text/csv');
  fs.createReadStream(file).pipe(res);
});

module.exports = router;
