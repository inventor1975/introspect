import express, { Request, Response } from 'express';
import validator from 'validator';

const app = express();

app.get('/orders/link', (req: Request, res: Response) => {
  const id = String(req.query.id ?? '');
  if (!validator.isUUID(id, 4)) {
    res.status(400).send('<p>That does not look like an order id.</p>');
    return;
  }
  res.send(`<p>Your order is ready: <a href="/orders/${id}">view order ${id}</a></p>`);
});

export default app;
