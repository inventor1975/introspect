const express = require('express');
const { execFile } = require('child_process');

const app = express();
app.use(express.json());

const MIRROR_ROOT = '/srv/repos/mirror';

app.post('/repos/check-remote', (req, res) => {
  const { remote, ref } = req.body;
  if (!remote) return res.status(400).json({ error: 'remote required' });
  execFile('git', ['ls-remote', remote, ref || 'HEAD'], { cwd: MIRROR_ROOT, timeout: 20000 }, (err, stdout) => {
    if (err) return res.status(422).json({ reachable: false });
    const refs = stdout.trim().split('\n').map((l) => {
      const [sha, name] = l.split('\t');
      return { sha, name };
    });
    res.json({ reachable: true, refs });
  });
});

module.exports = app;
