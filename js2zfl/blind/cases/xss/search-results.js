const express = require('express');
const router = express.Router();

router.get('/search', (req, res) => {
  const term = req.query.q || '';
  const page = parseInt(req.query.page, 10) || 1;
  res.send(`
    <h1>Results for ${term}</h1>
    <p>Page ${page}</p>
    <a href="/search?q=&page=${page + 1}">Next</a>
  `);
});

module.exports = router;
