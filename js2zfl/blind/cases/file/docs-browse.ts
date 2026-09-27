import express, { Request, Response } from 'express';
import * as fs from 'node:fs';
import * as path from 'node:path';

const DOCS_ROOT = path.resolve(__dirname, '../docs');
const app = express();

function toDocPath(input: string): string | null {
  const normalized = path.posix.normalize(input.replace(/\\/g, '/'));
  if (normalized.split('/').includes('..') || path.posix.isAbsolute(normalized) || normalized.includes('\0')) {
    return null;
  }
  return path.join(DOCS_ROOT, normalized);
}

app.get('/docs/raw', (req: Request, res: Response) => {
  const requested = typeof req.query.path === 'string' ? req.query.path : 'README.md';
  const docPath = toDocPath(requested);
  if (docPath === null) {
    res.status(400).json({ error: 'invalid document path' });
    return;
  }
  fs.readFile(docPath, 'utf8', (err, text) => {
    if (err) {
      res.status(404).json({ error: `${requested} not found` });
      return;
    }
    res.type('text/markdown').send(text);
  });
});

export default app;
