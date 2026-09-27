const express = require('express');
const path = require('path');

const PUBLIC_DIR = path.join(__dirname, 'public', 'downloads');
const router = express.Router();

router.get('/downloads/:name', (req, res, next) => {
  res.sendFile(req.params.name, { root: PUBLIC_DIR, dotfiles: 'deny' }, (err) => {
    if (err) next(err);
  });
});

module.exports = router;
