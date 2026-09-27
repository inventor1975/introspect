const express = require('express');
const { rebuildCache } = require('./lib/maintenance');

const router = express.Router();

router.post('/cache/rebuild', express.json(), (req, res) => {
  const reason = req.body.reason || 'manual';
  rebuildCache(reason, (err, output) => {
    if (err) return res.status(500).json({ error: 'rebuild failed' });
    res.json({ reason, output });
  });
});

module.exports = router;
