const express = require('express');
const fs = require('fs');
const path = require('path');

const SCRATCH = path.join(__dirname, 'scratch');

const operations = {
  read: (p) => fs.promises.readFile(p, 'utf8'),
  remove: (p) => fs.promises.unlink(p).then(() => 'removed'),
  info: (p) => fs.promises.stat(p).then((s) => ({ size: s.size, modified: s.mtime })),
};

const router = express.Router();

router.post('/scratch/op', express.json(), async (req, res) => {
  const handler = operations[req.body.op];
  if (typeof handler !== 'function') {
    return res.status(400).json({ error: 'unsupported op' });
  }
  try {
    const result = await handler(path.join(SCRATCH, req.body.target));
    res.json({ result });
  } catch (err) {
    res.status(500).json({ error: err.code || 'failed' });
  }
});

module.exports = router;
