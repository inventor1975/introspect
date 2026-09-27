import express, { Request, Response } from 'express';

const app = express();

app.get('/welcome-back', (req: Request, res: Response) => {
  let headline = req.query.headline as string;
  if (req.query.returning === '1') {
    headline = 'Welcome back!';
  } else {
    headline = 'Welcome!';
  }
  res.send(`<h1>${headline}</h1>`);
});

export default app;
