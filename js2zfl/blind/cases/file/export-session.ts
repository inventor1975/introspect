import express, { Request, Response } from 'express';
import session from 'express-session';
import { writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

declare module 'express-session' {
  interface SessionData {
    exportDir?: string;
  }
}

const EXPORT_ROOT = '/srv/exports';
const app = express();
app.use(express.json());
app.use(session({ secret: process.env.SESSION_SECRET ?? 'dev', resave: false, saveUninitialized: false }));

app.post('/exports/target', (req: Request, res: Response) => {
  req.session.exportDir = req.body.directory;
  res.json({ ok: true });
});

app.post('/exports/run', async (req: Request, res: Response) => {
  const dir = path.join(EXPORT_ROOT, req.session.exportDir ?? 'default');
  await mkdir(dir, { recursive: true });
  const rows = [['id', 'total'], ['1', '42.00']];
  const file = path.join(dir, `export-${Date.now()}.csv`);
  await writeFile(file, rows.map((r) => r.join(',')).join('\n'));
  res.status(201).json({ file: path.basename(file) });
});

export default app;
