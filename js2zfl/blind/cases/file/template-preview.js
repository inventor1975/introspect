const express = require('express');
const fs = require('fs');
const path = require('path');

const TEMPLATES = path.join(__dirname, 'templates', 'email');
const router = express.Router();

function cleanName(name) {
  return name.replace('../', '').replace(/^\/+/, '');
}

router.get('/templates/preview', (req, res) => {
  const name = cleanName(String(req.query.t || 'welcome.html'));
  const source = fs.readFileSync(path.join(TEMPLATES, name), 'utf8');
  res.json({ name, length: source.length, source });
});

module.exports = router;
