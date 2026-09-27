'use strict';

const express = require('express');
const fs = require('fs');
const path = require('path');
const { archiveRoot, regions } = require('./config/storage.json');

const router = express.Router();

router.get('/reports/:region/:year', (req, res) => {
  const region = req.params.region;
  const year = parseInt(req.params.year, 10);
  if (!regions.includes(region) || !Number.isInteger(year) || year < 2000 || year > 2100) {
    return res.status(400).json({ error: 'unknown region or year' });
  }
  const file = path.join(archiveRoot, region, `${year}.pdf`);
  fs.access(file, fs.constants.R_OK, (err) => {
    if (err) return res.sendStatus(404);
    res.sendFile(file);
  });
});

module.exports = router;
