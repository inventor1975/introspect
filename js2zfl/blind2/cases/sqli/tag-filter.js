'use strict';

const express = require('express');
const knex = require('knex')({ client: 'pg', connection: process.env.PG_URL });

const router = express.Router();

router.get('/notes/filter', async (req, res) => {
  const category = req.query.category;
  const rows = await knex.raw(
    `SELECT id, title FROM notes WHERE category = '${category}' AND archived = false`
  );
  res.json(rows.rows);
});

module.exports = router;
