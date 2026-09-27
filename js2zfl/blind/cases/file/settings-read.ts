import express, { Request, Response } from 'express';
import { readFile } from 'node:fs/promises';
import path from 'node:path';

const SETTINGS_FILE = path.join(__dirname, 'config', 'public-settings.json');
const app = express();

app.get('/settings', async (req: Request, res: Response) => {
  const key = req.query.key as string | undefined;
  const raw = await readFile(SETTINGS_FILE, 'utf8');
  const settings: Record<string, unknown> = JSON.parse(raw);
  if (!key) {
    res.json(settings);
    return;
  }
  if (!Object.prototype.hasOwnProperty.call(settings, key)) {
    res.status(404).json({ error: 'unknown setting' });
    return;
  }
  res.json({ key, value: settings[key] });
});

export default app;
