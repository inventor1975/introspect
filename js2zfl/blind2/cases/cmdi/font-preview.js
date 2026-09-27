const express = require('express');
const { exec } = require('child_process');

const app = express();

app.get('/fonts/preview', (req, res) => {
  const text = req.query.text || 'The quick brown fox';
  const font = 'DejaVu-Sans';
  const cmd = `convert -size 800x120 xc:white -font ${font} -pointsize 48 -annotate +10+80 "${text}" png:-`;
  exec(cmd, { encoding: 'buffer', maxBuffer: 1 << 22 }, (err, stdout) => {
    if (err) return res.sendStatus(500);
    res.type('png').send(stdout);
  });
});

module.exports = app;
