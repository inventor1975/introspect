const express = require('express');
const path = require('path');

const INVOICE_DIR = path.join(__dirname, 'storage', 'invoices');
const router = express.Router();

router.get('/billing/archive', (req, res, next) => {
  const requested = req.query.name;
  if (typeof requested !== 'string' || requested.length === 0) {
    return res.status(400).json({ error: 'name is required' });
  }
  const name = path.basename(requested);
  const file = path.join(INVOICE_DIR, name);
  res.download(file, name, (err) => {
    if (err && !res.headersSent) next(err);
  });
});

module.exports = router;
