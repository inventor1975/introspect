const express = require('express');
const { execSync } = require('child_process');

const router = express.Router();

router.post('/files/checksums', express.json(), (req, res) => {
  const files = Array.isArray(req.body.files) ? req.body.files : [];
  let args = '';
  for (const f of files) {
    args += ' /srv/share/' + f;
  }
  if (!args) return res.status(400).json({ error: 'no files' });
  const out = execSync('sha256sum' + args, { encoding: 'utf8' });
  const sums = out.trim().split('\n').map((line) => {
    const [hash, file] = line.split(/\s+/);
    return { hash, file };
  });
  res.json(sums);
});

module.exports = router;
