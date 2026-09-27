'use strict';

const express = require('express');
const sqlite3 = require('sqlite3');

const app = express();
const db = new sqlite3.Database('./chat.db');

app.get('/rooms/:room/messages', (req, res) => {
  const room = req.params.room;
  const sql =
    'SELECT sender, text, ts FROM messages WHERE room = ? ORDER BY ts ASC LIMIT 100';
  db.all(sql, [room], (err, rows) => {
    if (err) return res.status(500).end();
    res.json(rows);
  });
});

module.exports = app;
