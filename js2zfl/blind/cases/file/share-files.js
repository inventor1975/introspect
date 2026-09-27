const express = require('express');
const fs = require('fs');
const { safeJoin, PathEscapeError } = require('./lib/path-guard');

const SHARE_ROOT = process.env.SHARE_ROOT || '/srv/share';
const router = express.Router();

router.get('/share/*', (req, res, next) => {
  let target;
  try {
    target = safeJoin(SHARE_ROOT, req.params[0]);
  } catch (err) {
    if (err instanceof PathEscapeError) return res.status(err.status).send('Forbidden');
    return next(err);
  }
  fs.createReadStream(target)
    .on('error', () => res.status(404).end())
    .pipe(res);
});

module.exports = router;
