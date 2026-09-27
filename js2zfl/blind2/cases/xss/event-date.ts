import express, { Request, Response } from 'express';

const app = express();

app.get('/events/on', (req: Request, res: Response) => {
  const when = new Date(String(req.query.date ?? ''));
  if (Number.isNaN(when.getTime())) {
    res.status(400).send('<p>Please pick a valid date.</p>');
    return;
  }
  res.send(`<p>Events on <time datetime="${when.toISOString()}">${when.toUTCString()}</time></p>`);
});

export default app;
