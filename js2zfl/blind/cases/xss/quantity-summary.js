const express = require('express');

const app = express();

app.get('/cart/summary', (req, res) => {
  const qty = parseInt(req.query.qty, 10);
  const unit = Number.parseFloat(req.query.unitPrice);
  if (Number.isNaN(qty) || Number.isNaN(unit)) {
    return res.status(400).send('<p>Invalid input</p>');
  }
  const total = (qty * unit).toFixed(2);
  res.send('<p>You are buying ' + qty + ' item(s) for $' + total + '</p>');
});

module.exports = app;
