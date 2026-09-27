const express = require('express');
const { toLabel } = require('./lib/slug');

const router = express.Router();

router.get('/collections/:name', (req, res) => {
  const label = toLabel(req.params.name);
  const subtitle = toLabel(req.query.subtitle);
  res.send(`<header class="collection"><h1>${label}</h1><p>${subtitle}</p></header>`);
});

module.exports = router;
