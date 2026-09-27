import express from 'express';
import path from 'node:path';
import { readFile } from 'node:fs/promises';

const app = express();
const DATA_ROOT = path.resolve('/srv/app/data');

app.get('/tenant/files', async (req, res) => {
  const requested = req.query.file as string;
  const target = path.resolve(DATA_ROOT, requested);
  if (!target.startsWith(DATA_ROOT)) {
    res.status(403).json({ error: 'outside data root' });
    return;
  }
  try {
    const content = await readFile(target);
    res.type(path.extname(target) || 'bin').send(content);
  } catch {
    res.sendStatus(404);
  }
});

export default app;
