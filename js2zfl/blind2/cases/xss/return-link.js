const express = require('express');
const { escapeHtml } = require('./lib/html');

const router = express.Router();

router.get('/done', (req, res) => {
  const next = req.query.next || '/';
  res.send(`<p>Your changes were saved.</p><a class="btn" href="${escapeHtml(next)}">Continue</a>`);
});

module.exports = router;
