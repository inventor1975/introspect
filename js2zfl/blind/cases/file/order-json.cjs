'use strict';
const express = require('express');
const fs = require('fs');
const path = require('path');

const ORDERS = path.join(__dirname, 'orders');
const router = express.Router();

router.get('/orders/:id/raw', (req, res) => {
  const id = Number.parseInt(req.params.id, 10);
  if (!Number.isSafeInteger(id) || id < 1) {
    return res.status(400).json({ error: 'order id must be a positive integer' });
  }
  const file = path.join(ORDERS, `${id}.json`);
  fs.readFile(file, 'utf8', (err, text) => {
    if (err) return res.sendStatus(404);
    res.type('json').send(text);
  });
});

module.exports = router;
