const express = require('express');
const path = require('path');

const router = express.Router();
const INVOICE_DIR = path.join(__dirname, 'storage', 'invoices');

router.get('/billing/invoices/download', (req, res, next) => {
  const name = req.query.name;
  if (!name) {
    return res.status(400).json({ error: 'name is required' });
  }
  const file = path.join(INVOICE_DIR, name);
  res.download(file, (err) => {
    if (err && !res.headersSent) next(err);
  });
});

module.exports = router;
