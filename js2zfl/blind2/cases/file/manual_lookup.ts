import express, { Request, Response } from 'express';
import { readFile } from 'fs/promises';
import { join } from 'path';

const MANUALS_DIR = join(__dirname, 'manuals');

const MANUALS = new Map<string, string>([
  ['router-x1', 'router-x1-v3.pdf'],
  ['switch-s24', 'switch-s24-v1.pdf'],
  ['ap-mini', 'ap-mini-v2.pdf'],
]);

const app = express();

app.get('/support/manual', async (req: Request, res: Response) => {
  const model = String(req.query.model || '');
  const fileName = MANUALS.get(model);
  if (fileName === undefined) {
    res.status(404).json({ error: `no manual for ${model}` });
    return;
  }
  const pdf = await readFile(join(MANUALS_DIR, fileName));
  res.type('application/pdf').send(pdf);
});

export default app;
