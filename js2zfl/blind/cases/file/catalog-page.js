const express = require('express');
const fs = require('fs');

const CATALOG_DIR = __dirname + '/catalog';
const MAX_PAGE = 50;
const app = express();

app.get('/catalog', (req, res) => {
  const page = Math.max(1, Math.min(MAX_PAGE, Number(req.query.page) || 1));
  const html = fs.readFileSync(`${CATALOG_DIR}/page-${page}.html`, 'utf8');
  res.set('X-Page', String(page)).type('html').send(html);
});

module.exports = app;
