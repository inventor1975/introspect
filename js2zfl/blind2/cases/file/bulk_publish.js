const express = require('express');
const fs = require('fs');
const path = require('path');

const router = express.Router();
const STAGING = '/srv/cms/staging';
const LIVE = '/srv/cms/live';

router.post('/cms/publish', express.json(), async (req, res) => {
  const files = Array.isArray(req.body.files) ? req.body.files : [];
  const published = [];
  for (const entry of files) {
    const from = path.join(STAGING, entry);
    const to = path.join(LIVE, entry);
    await fs.promises.mkdir(path.dirname(to), { recursive: true });
    await fs.promises.copyFile(from, to);
    published.push(entry);
  }
  res.json({ published });
});

module.exports = router;
