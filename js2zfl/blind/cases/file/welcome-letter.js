const express = require('express');
const fs = require('fs');
const path = require('path');

const TEMPLATE = path.join(__dirname, 'templates', 'welcome-letter.txt');
const OUTBOX = path.join(__dirname, 'outbox');
const router = express.Router();
router.use(express.urlencoded({ extended: false }));

router.post('/letters/welcome', (req, res) => {
  const name = String(req.body.name || 'customer');
  const company = String(req.body.company || '');
  const template = fs.readFileSync(TEMPLATE, 'utf8');
  const letter = template.replace('{{name}}', name).replace('{{company}}', company);
  const outFile = path.join(OUTBOX, `welcome-${Date.now()}-${process.pid}.txt`);
  fs.writeFile(outFile, letter, (err) => {
    if (err) return res.status(500).json({ error: 'could not queue letter' });
    res.status(202).json({ queued: path.basename(outFile), recipient: name });
  });
});

module.exports = router;
