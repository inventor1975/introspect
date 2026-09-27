'use strict';

const express = require('express');
const mysql = require('mysql2');

const router = express.Router();
const conn = mysql.createConnection({ database: 'tasks' });

router.post('/tasks/status', (req, res) => {
  const { id, done } = req.body;
  let sql;
  if (done === 'true') {
    sql = 'UPDATE tasks SET status = "done" WHERE id = ' + id;
  } else {
    sql = 'UPDATE tasks SET status = "open" WHERE id = ' + id;
  }
  conn.query(sql, (err) => {
    if (err) return res.sendStatus(500);
    res.sendStatus(204);
  });
});

module.exports = router;
