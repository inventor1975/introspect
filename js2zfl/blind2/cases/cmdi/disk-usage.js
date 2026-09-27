const express = require('express');
const util = require('util');
const cp = require('child_process');

const run = util.promisify(cp.exec);
const app = express();

app.get('/storage/usage', async (req, res) => {
  const volume = req.query.volume || '/';
  try {
    const { stdout } = await run('df -h ' + volume + ' | tail -1');
    const [fs, size, used, avail, pct] = stdout.trim().split(/\s+/);
    res.json({ fs, size, used, avail, pct });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = app;
