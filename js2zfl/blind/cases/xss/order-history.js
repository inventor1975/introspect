const express = require('express');
const escapeHtml = require('escape-html');

const router = express.Router();

router.get('/orders', (req, res) => {
  const customer = req.query.customer || '';
  const status = req.query.status || 'all';
  res.send(`
    <h1>Orders for ${escapeHtml(customer)}</h1>
    <p>Showing: ${escapeHtml(status)}</p>
    <table id="orders"></table>
  `);
});

module.exports = router;
