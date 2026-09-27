import express from 'express';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FILES_ROOT = path.join(__dirname, 'files');

const app = express();

app.get('/files/*', (req, res) => {
  const relative = req.params[0];
  const absolute = path.join(FILES_ROOT, relative);
  res.sendFile(absolute, { dotfiles: 'allow' }, (err) => {
    if (err) res.status(err.status || 500).end();
  });
});

export default app;
