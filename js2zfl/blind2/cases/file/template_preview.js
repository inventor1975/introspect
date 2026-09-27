const express = require('express');
const fs = require('fs');
const path = require('path');

const router = express.Router();
const TEMPLATE_ROOT = path.join(__dirname, 'mail-templates');

function stripTraversal(input) {
  return input.replace('../', '');
}

router.get('/admin/mail/preview', (req, res) => {
  const name = stripTraversal(String(req.query.template || 'welcome.html'));
  fs.readFile(path.join(TEMPLATE_ROOT, name), 'utf8', (err, html) => {
    if (err) {
      return res.status(404).send('Template not found');
    }
    res.set('Content-Type', 'text/plain; charset=utf-8');
    res.send(html);
  });
});

module.exports = router;
