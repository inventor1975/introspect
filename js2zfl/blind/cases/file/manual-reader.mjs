import express from 'express';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MANUALS = path.join(__dirname, 'manuals');

export const manualRouter = express.Router();

manualRouter.get('/manual', async (req, res) => {
  const section = req.query.section ?? 'index.txt';
  let body;
  try {
    body = await readFile(path.join(MANUALS, section), 'utf8');
  } catch (err) {
    body = await readFile(path.join(MANUALS, 'index.txt'), 'utf8');
  }
  res.type('text/plain').send(body);
});
