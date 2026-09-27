'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'auth' });

router.post('/login', (req, res) => {
  const { username, password } = req.body;
  const sql =
    'SELECT id, role FROM users WHERE username = ? AND password_hash = ?';
  pool.execute(sql, [username, password], (err, rows) => {
    if (err) return res.sendStatus(500);
    res.json({ ok: rows.length > 0 });
  });
});

module.exports = router;
