'use strict';

const express = require('express');
const knex = require('knex')({ client: 'pg', connection: process.env.PG_URL });

const router = express.Router();

router.get('/translations', async (req, res) => {
  const locale = req.query.locale;
  const namespace = req.query.ns;
  const result = await knex.raw(
    'SELECT msg_key, msg_value FROM translations WHERE locale = :locale AND ns = :ns',
    { locale, ns: namespace }
  );
  res.json(result.rows);
});

module.exports = router;
