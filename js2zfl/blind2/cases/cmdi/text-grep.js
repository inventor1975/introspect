const express = require('express');
const { spawn } = require('child_process');

const router = express.Router();
const CORPUS = '/srv/corpus/all.txt';

router.get('/corpus/grep', (req, res) => {
  const term = String(req.query.term || '');
  if (!term) return res.status(400).end();
  const grep = spawn('grep', ['-F', '-i', '-m', '100', '--', term, CORPUS]);
  res.type('text/plain');
  grep.stdout.pipe(res);
  grep.on('error', () => res.end());
});

module.exports = router;
