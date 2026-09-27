import express, { Request, Response } from 'express';
import { stripScripts, collapseWhitespace } from './lib/strip';

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/newsletter/preview', (req: Request, res: Response) => {
  const draft: string = req.body.draft ?? '';
  const cleaned = collapseWhitespace(stripScripts(draft));
  res.send(`<div class="newsletter-preview">${cleaned}</div>`);
});

export default app;
