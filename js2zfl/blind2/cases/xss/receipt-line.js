const express = require('express');
const util = require('util');

const app = express();

app.get('/receipt/line', (req, res) => {
  const item = req.query.item;
  const amount = Number(req.query.amount || 0).toFixed(2);
  const row = util.format('<tr><td>%s</td><td class="num">%s</td></tr>', item, amount);
  res.send('<table class="receipt">' + row + '</table>');
});

module.exports = app;
