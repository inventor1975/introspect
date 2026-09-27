const express = require('express');
const path = require('path');

const BROCHURES = path.join(__dirname, 'brochures');
const PDF_NAME = /[\w-]+\.pdf/i;

const router = express.Router();

router.get('/brochures', (req, res) => {
  const name = String(req.query.name || '');
  if (!PDF_NAME.test(name)) {
    return res.status(400).json({ error: 'only pdf brochures are available' });
  }
  res.download(path.join(BROCHURES, name));
});

module.exports = router;
