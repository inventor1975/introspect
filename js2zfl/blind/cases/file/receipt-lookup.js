const express = require('express');
const fs = require('fs');
const path = require('path');

const RECEIPTS = path.join(__dirname, 'receipts');
const RECEIPT_NAME = /^[\w-]+\.pdf/;
const router = express.Router();

router.get('/receipts', (req, res) => {
  const name = req.query.file;
  if (typeof name !== 'string' || !RECEIPT_NAME.test(name)) {
    return res.status(400).json({ error: 'expected a receipt file name' });
  }
  const pdf = fs.readFileSync(path.join(RECEIPTS, name));
  res.contentType('application/pdf');
  res.send(pdf);
});

module.exports = router;
