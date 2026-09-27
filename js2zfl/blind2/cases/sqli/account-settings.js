'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'accounts' });

router.post('/settings/theme', (req, res) => {
  const theme = req.body.theme;
  const userId = req.body.userId;
  let statement = 'UPDATE preferences SET theme = "' + theme + '"';
  statement += ' WHERE user_id = ' + userId;
  conn.query(statement, (err) => {
    if (err) return res.sendStatus(500);
    res.sendStatus(204);
  });
});

module.exports = router;
