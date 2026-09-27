'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const pool = mysql.createPool({ database: 'inventory' });

router.post('/items/remove', (req, res) => {
  const ids = req.body.ids; // array of id strings
  const list = ids.join(', ');
  const sql = 'DELETE FROM items WHERE id IN (' + list + ')';
  pool.query(sql, (err, result) => {
    if (err) return res.status(500).json({ ok: false });
    res.json({ removed: result.affectedRows });
  });
});

module.exports = router;
