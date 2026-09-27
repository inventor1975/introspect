'use strict';

const express = require('express');
const knex = require('knex')({ client: 'pg', connection: process.env.PG_URL });

const router = express.Router();

router.get('/labels', async (req, res) => {
  const project = req.query.project;
  const result = await knex.raw(
    'SELECT id, name, color FROM labels WHERE project_id = ?',
    [project]
  );
  res.json(result.rows);
});

module.exports = router;
