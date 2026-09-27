'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'catalog' });

router.post('/products/batch', (req, res) => {
  const ids = req.body.ids; // array
  const placeholders = ids.map(() => '?').join(', ');
  const sql = 'SELECT id, title FROM products WHERE id IN (' + placeholders + ')';
  pool.query(sql, ids, (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json(rows);
  });
});

module.exports = router;
