import express from 'express';
import { readFile } from 'node:fs/promises';

const app = express();
const PUBLIC_BASE = new URL('./public/', import.meta.url);

app.get('/assets/resolve', async (req, res) => {
  const relative = req.query.p ?? 'index.html';
  const fileUrl = new URL(relative, PUBLIC_BASE);
  try {
    const data = await readFile(fileUrl);
    res.type(fileUrl.pathname.split('.').pop() || 'txt').send(data);
  } catch (err) {
    res.status(404).json({ error: 'asset missing' });
  }
});

export default app;
