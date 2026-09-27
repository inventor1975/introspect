const express = require('express');
const fs = require('fs');
const path = require('path');

const STATEMENTS = '/srv/bank/statements';
const STATEMENT_NAME = /^[A-Za-z0-9_-]{1,64}\.pdf$/;

const router = express.Router();

router.get('/statements', (req, res) => {
  const name = req.query.name;
  if (typeof name !== 'string' || !STATEMENT_NAME.test(name)) {
    return res.status(400).json({ error: 'invalid statement name' });
  }
  const location = path.join(STATEMENTS, name);
  res.setHeader('Content-Type', 'application/pdf');
  fs.createReadStream(location)
    .on('error', () => res.status(404).end())
    .pipe(res);
});

module.exports = router;
