import express, { Request, Response } from 'express';
import { readFileSync } from 'fs';
import { join } from 'path';

const LOCALES_DIR = join(__dirname, 'locales');
const SUPPORTED = ['en', 'de', 'fr', 'es', 'pt-BR', 'ja'] as const;

const app = express();

app.get('/i18n/:lang', (req: Request, res: Response) => {
  const lang = req.params.lang;
  if (!(SUPPORTED as readonly string[]).includes(lang)) {
    res.status(404).json({ error: `unsupported locale ${lang}` });
    return;
  }
  const bundle = readFileSync(join(LOCALES_DIR, `${lang}.json`), 'utf8');
  res.type('application/json').send(bundle);
});

export default app;
