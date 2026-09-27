const express = require('express');
const escapeHtml = require('escape-html');

const router = express.Router();

router.get('/catalog', (req, res) => {
  const encoded = String(req.query.label || 'All items');
  const label = decodeURIComponent(escapeHtml(encoded));
  res.send(`<h3 class="filter">${label}</h3><ul id="items"></ul>`);
});

module.exports = router;
