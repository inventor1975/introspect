import express, { Request, Response } from 'express';
import ejs from 'ejs';

const app = express();

const CARD = `
<div class="card">
  <h1><%= occasion %></h1>
  <p><%- message %></p>
</div>`;

app.get('/card', (req: Request, res: Response) => {
  const occasion = String(req.query.occasion || 'Happy birthday');
  const message = String(req.query.message || '');
  res.send(ejs.render(CARD, { occasion, message }));
});

export default app;
