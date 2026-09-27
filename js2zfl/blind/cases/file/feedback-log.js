const express = require('express');
const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(__dirname, 'var', 'log');
const FEEDBACK_LOG = path.join(LOG_DIR, 'feedback.log');
const app = express();
app.use(express.json());

app.post('/feedback', (req, res) => {
  const { page, rating, message } = req.body;
  const entry = JSON.stringify({ at: Date.now(), page, rating, message }) + '\n';
  fs.appendFile(FEEDBACK_LOG, entry, { encoding: 'utf8' }, (err) => {
    if (err) return res.status(500).json({ error: 'could not record feedback' });
    res.status(202).json({ thanks: true, page });
  });
});

module.exports = app;
