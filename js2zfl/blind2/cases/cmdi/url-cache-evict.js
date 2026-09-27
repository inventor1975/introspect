const express = require('express');
const crypto = require('crypto');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

app.post('/proxy-cache/evict', (req, res) => {
  const url = req.body.url;
  if (!url) return res.status(400).json({ error: 'url required' });
  const key = crypto.createHash('sha256').update(url).digest('hex');
  exec(`rm -f /var/cache/proxy/${key.slice(0, 2)}/${key}`, (err) => {
    res.json({ url, key, evicted: !err });
  });
});

module.exports = app;
