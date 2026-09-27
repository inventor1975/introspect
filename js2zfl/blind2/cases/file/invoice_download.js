const express = require('express');
const path = require('path');

const router = express.Router();
const INVOICE_DIR = path.join(__dirname, '..', 'storage', 'invoices');

router.get('/billing/invoices/download', (req, res, next) => {
  const requested = req.query.file;
  if (!requested) {
    return res.status(400).json({ error: 'file is required' });
  }
  const fullPath = path.join(INVOICE_DIR, requested);
  res.download(fullPath, (err) => {
    if (err && !res.headersSent) {
      next(err);
    }
  });
});

module.exports = router;
