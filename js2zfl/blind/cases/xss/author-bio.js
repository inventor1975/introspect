const express = require('express');
const pool = require('./lib/db');

const router = express.Router();

router.get('/authors/:id', async (req, res, next) => {
  try {
    const { rows } = await pool.query(
      'SELECT display_name, bio FROM authors WHERE id = $1',
      [req.params.id]
    );
    if (rows.length === 0) return res.status(404).send('<p>Unknown author</p>');
    const author = rows[0];
    res.send(`<section><h2>${author.display_name}</h2><div class="bio">${author.bio}</div></section>`);
  } catch (e) {
    next(e);
  }
});

module.exports = router;
