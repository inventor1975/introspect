import express from 'express';
import session from 'express-session';
import { exec } from 'child_process';

declare module 'express-session' {
  interface SessionData {
    workspace?: string;
  }
}

const app = express();
app.use(express.json());
app.use(session({ secret: process.env.SESSION_SECRET || 'dev', resave: false, saveUninitialized: false }));

app.post('/workspace/select', (req, res) => {
  req.session.workspace = req.body.workspace;
  res.sendStatus(204);
});

app.get('/workspace/files', (req, res) => {
  const ws = req.session.workspace || 'default';
  exec(`ls -1 /srv/workspaces/${ws}`, (err, stdout) => {
    if (err) return res.status(404).json({ error: 'not found' });
    res.json(stdout.trim().split('\n'));
  });
});

export default app;
