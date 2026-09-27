import express, { Request, Response } from 'express';

const app = express();

const HEX_COLOR = /#?[0-9a-f]{6}/i;

app.get('/swatch', (req: Request, res: Response) => {
  const color = String(req.query.color || '#336699');
  if (!HEX_COLOR.test(color)) {
    res.status(400).send('<p>Invalid colour.</p>');
    return;
  }
  res.send(`<div class="swatch">Selected: ${color}</div>`);
});

export default app;
