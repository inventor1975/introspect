import express, { Request, Response } from 'express';
import { execFile } from 'child_process';

const app = express();
const SEMVER = /^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$/;

app.get('/runtime/compare', (req: Request, res: Response) => {
  const wanted = String(req.query.version || '');
  const match = SEMVER.exec(wanted);
  if (!match) {
    return res.status(400).json({ error: `not a version: ${wanted}` });
  }
  execFile('node', ['--version'], (err, stdout) => {
    if (err) return res.sendStatus(500);
    const current = SEMVER.exec(stdout.trim());
    const major = current ? Number(current[1]) : 0;
    res.json({ current: stdout.trim(), wanted, compatible: major >= Number(match[1]) });
  });
});

export default app;
