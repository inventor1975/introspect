const express = require('express');
const { spawn } = require('child_process');

const app = express();
app.use(express.text({ limit: '1mb' }));

app.post('/text/stats', (req, res) => {
  const wc = spawn('wc', ['-l', '-w', '-c']);
  let out = '';
  wc.stdout.on('data', (d) => { out += d; });
  wc.on('close', () => {
    const [lines, words, bytes] = out.trim().split(/\s+/).map(Number);
    res.json({ lines, words, bytes });
  });
  wc.stdin.write(req.body);
  wc.stdin.end();
});

module.exports = app;
