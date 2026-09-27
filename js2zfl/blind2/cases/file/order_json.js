const express = require('express');
const fs = require('fs');
const path = require('path');

const ORDERS_DIR = path.join(__dirname, 'orders');
const app = express();

app.get('/orders/:orderId', (req, res) => {
  const orderId = parseInt(req.params.orderId, 10);
  if (Number.isNaN(orderId) || orderId <= 0) {
    return res.status(400).json({ error: 'invalid order id' });
  }
  const file = path.join(ORDERS_DIR, `${orderId}.json`);
  fs.readFile(file, 'utf8', (err, text) => {
    if (err) return res.sendStatus(404);
    res.type('json').send(text);
  });
});

module.exports = app;
