import express from 'express';
import { execFile } from 'child_process';

const app = express();
const REPO = '/srv/repos/main';

app.get('/history', (req, res) => {
  const count = Math.min(Math.max(Number(req.query.count) || 20, 1), 500);
  const file = typeof req.query.path === 'string' ? req.query.path : '.';
  execFile(
    'git',
    ['-C', REPO, 'log', '--format=%H%x09%an%x09%s', '-n', String(count), '--', file],
    { maxBuffer: 8 * 1024 * 1024 },
    (err, stdout) => {
      if (err) return res.status(500).json({ error: 'git log failed' });
      res.json(stdout.trim().split('\n').map((l) => l.split('\t')));
    },
  );
});

export default app;
