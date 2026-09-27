'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'shop' });

router.get('/orders/detail', (req, res) => {
  const orderId = parseInt(req.query.id, 10);
  if (Number.isNaN(orderId)) return res.status(400).json({ error: 'bad id' });
  // orderId is a verified integer; no string can survive parseInt.
  const sql = 'SELECT id, total, status FROM orders WHERE id = ' + orderId;
  conn.query(sql, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows[0] || {});
  });
});

module.exports = router;
