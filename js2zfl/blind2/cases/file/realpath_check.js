const express = require('express');
const fs = require('fs');
const path = require('path');

const PROJECTS_ROOT = fs.realpathSync(path.join(__dirname, 'projects'));
const router = express.Router();

router.get('/projects/source', async (req, res) => {
  const requested = path.join(PROJECTS_ROOT, String(req.query.file || ''));
  let real;
  try {
    real = await fs.promises.realpath(requested);
  } catch (e) {
    return res.sendStatus(404);
  }
  if (!real.startsWith(PROJECTS_ROOT + path.sep)) {
    return res.sendStatus(403);
  }
  const source = await fs.promises.readFile(real, 'utf8');
  res.type('text/plain').send(source);
});

module.exports = router;
