import express, { Request, Response } from 'express';
import session from 'express-session';
import { readdir } from 'fs/promises';
import * as path from 'path';
import { verifyCredentials } from './lib/accounts';

declare module 'express-session' {
  interface SessionData {
    workspace?: string;
    userId?: number;
  }
}

const WORKSPACES = '/srv/workspaces';
const app = express();

app.use(express.json());
app.use(session({ secret: process.env.SESSION_SECRET as string, resave: false, saveUninitialized: false }));

app.post('/login', async (req: Request, res: Response) => {
  const user = await verifyCredentials(req.body.email, req.body.password);
  if (!user) {
    res.sendStatus(401);
    return;
  }
  req.session.userId = user.id;
  req.session.workspace = req.body.workspace || user.defaultWorkspace;
  res.json({ ok: true });
});

app.get('/workspace/files', async (req: Request, res: Response) => {
  if (!req.session.userId || !req.session.workspace) {
    res.sendStatus(401);
    return;
  }
  const entries = await readdir(path.join(WORKSPACES, req.session.workspace));
  res.json({ entries });
});

export default app;
