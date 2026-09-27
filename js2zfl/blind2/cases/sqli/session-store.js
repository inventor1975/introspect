'use strict';

const express = require('express');
const Database = require('better-sqlite3');

const router = express.Router();
const db = new Database('sessions.db');

router.get('/sessions/find', (req, res) => {
  const token = req.query.token;
  const stmt = db.prepare(
    "SELECT user_id, expires FROM sessions WHERE token = '" + token + "'"
  );
  const row = stmt.get();
  res.json(row || {});
});

module.exports = router;
