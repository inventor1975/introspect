'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ host: 'localhost', database: 'app' });

router.get('/users/lookup', (req, res) => {
  const id = req.query.id;
  const sql = `SELECT id, email, display_name FROM users WHERE id = ${id}`;
  conn.query(sql, (err, rows) => {
    if (err) return res.status(500).json({ error: 'lookup failed' });
    res.json(rows);
  });
});

module.exports = router;
