import express, { Request, Response } from 'express';
import * as fs from 'fs';
import * as path from 'path';

const LABELS_DIR = path.join(__dirname, 'shipping-labels');
const router = express.Router();

function isPlainFileName(name: unknown): name is string {
  if (typeof name !== 'string' || name.length === 0 || name.length > 128) return false;
  if (name.includes('..') || name.includes('/') || name.includes('\\') || name.includes('\0')) return false;
  return !path.isAbsolute(name);
}

router.delete('/labels/:name', (req: Request, res: Response) => {
  const name = req.params.name;
  if (!isPlainFileName(name)) {
    res.status(400).json({ error: 'invalid label name' });
    return;
  }
  fs.unlink(path.join(LABELS_DIR, name), (err) => {
    if (err) {
      res.sendStatus(err.code === 'ENOENT' ? 404 : 500);
      return;
    }
    res.sendStatus(204);
  });
});

export default router;
