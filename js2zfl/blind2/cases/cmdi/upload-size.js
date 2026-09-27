const express = require('express');
const path = require('path');
const { exec } = require('child_process');

const router = express.Router();

router.get('/uploads/size', (req, res) => {
  const name = path.basename(req.query.file || '');
  if (!name) return res.status(400).end();
  exec(`du -sh /srv/uploads/${name}`, (err, stdout) => {
    if (err) return res.status(404).end();
    res.json({ size: stdout.split('\t')[0] });
  });
});

module.exports = router;
