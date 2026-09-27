const express = require('express');

const router = express.Router();
router.use(express.urlencoded({ extended: false }));

router.post('/import/preview', (req, res) => {
  const raw = req.body.payload;
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (err) {
    return res
      .status(400)
      .send(`<h2>Could not parse import</h2><pre>${raw}</pre><p>${err.message}</p>`);
  }
  res.send(`<p>Parsed ${Object.keys(parsed).length} fields.</p>`);
});

module.exports = router;
