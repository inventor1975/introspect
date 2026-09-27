const express = require('express');
const { exec } = require('child_process');
const { quote } = require('shell-quote');

const app = express();

app.get('/datasets/lines', (req, res) => {
  const dataset = req.query.dataset;
  const file = `/srv/datasets/${dataset}.csv`;
  exec(`wc -l ${quote([file])}`, (err, stdout) => {
    if (err) return res.status(404).json({ error: 'dataset not found' });
    res.json({ dataset, lines: parseInt(stdout, 10) });
  });
});

module.exports = app;
