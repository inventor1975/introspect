const express = require('express');
const _ = require('lodash');

const app = express();

const receipt = _.template(
  '<div class="receipt"><h2>Thanks, <%= customer %>!</h2><p>Order #<%- orderId %></p></div>'
);

app.get('/receipt', (req, res) => {
  const html = receipt({ customer: req.query.customer, orderId: req.query.order });
  res.send(html);
});

module.exports = app;
