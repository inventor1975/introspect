'use strict';

const express = require('express');
const knex = require('knex')({ client: 'mysql2', connection: {} });

const router = express.Router();

router.get('/catalog/price', async (req, res) => {
  const min = req.query.min;
  const max = req.query.max;
  const rows = await knex('products')
    .select('id', 'title', 'price')
    .whereRaw('price BETWEEN ' + min + ' AND ' + max);
  res.json(rows);
});

module.exports = router;
