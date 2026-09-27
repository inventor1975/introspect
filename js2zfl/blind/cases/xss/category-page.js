const express = require('express');

const router = express.Router();

router.param('category', (req, res, next, value) => {
  req.category = value.toLowerCase();
  next();
});

router.get('/c/:category', (req, res) => {
  res.send(`<h1>Browsing ${req.category}</h1><div id="grid"></div>`);
});

module.exports = router;
