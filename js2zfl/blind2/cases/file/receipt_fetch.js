const express = require('express');
const fs = require('fs');
const path = require('path');

const RECEIPTS = path.join(__dirname, 'storage', 'receipts');
const router = express.Router();

router.get('/receipts/:file', (req, res) => {
  const fileName = path.basename(req.params.file);
  const location = path.join(RECEIPTS, fileName);
  fs.readFile(location, (err, pdf) => {
    if (err) {
      return res.status(404).json({ error: `receipt ${fileName} not found` });
    }
    res.type('application/pdf').send(pdf);
  });
});

module.exports = router;
