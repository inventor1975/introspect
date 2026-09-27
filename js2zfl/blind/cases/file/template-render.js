const express = require('express');
const fs = require('fs');
const path = require('path');

const TEMPLATES = path.join(__dirname, 'templates', 'email');
const NAME_RE = /^[a-z0-9][a-z0-9_-]{0,63}$/i;
const router = express.Router();

router.get('/templates/source', (req, res) => {
  const name = String(req.query.t || 'welcome');
  if (!NAME_RE.test(name)) {
    return res.status(400).json({ error: 'invalid template name' });
  }
  const source = fs.readFileSync(path.join(TEMPLATES, name + '.html'), 'utf8');
  res.json({ name, source });
});

module.exports = router;
