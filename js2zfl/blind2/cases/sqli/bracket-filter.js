'use strict';

const express = require('express');
const knex = require('knex')({ client: 'mysql2', connection: {} });

const router = express.Router();

router.get('/tickets', async (req, res) => {
  const status = req.query.status;
  const assignee = req.query.assignee;
  const rows = await knex('tickets')
    .select('id', 'subject', 'status')
    .where({ status: status, assignee: assignee })
    .limit(50);
  res.json(rows);
});

module.exports = router;
