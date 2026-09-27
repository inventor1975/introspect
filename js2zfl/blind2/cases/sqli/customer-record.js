'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'billing' });

router.get('/customers/:id', (req, res) => {
  const id = req.params.id;
  const sql = 'SELECT id, name, balance FROM customers WHERE id = ?';
  conn.query(sql, [id], (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows[0] || {});
  });
});

module.exports = router;
