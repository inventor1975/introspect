import express, { Request, Response } from 'express';
import escapeHtml from 'escape-html';

const app = express();

app.get('/hello', (req: Request, res: Response) => {
  const raw = String(req.query.name || 'friend');
  let shown: string;
  if (req.query.format === 'plain') {
    shown = escapeHtml(raw);
  } else if (req.query.format === 'upper') {
    shown = escapeHtml(raw.toUpperCase());
  } else {
    shown = raw.trim();
  }
  res.send(`<h1>Hello, ${shown}</h1>`);
});

export default app;
