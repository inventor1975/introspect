import express, { Request, Response } from 'express';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

type Props = { customer: string; note?: string };

function OrderSummary({ customer, note }: Props) {
  return (
    <section className="order-summary">
      <h2>Order for {customer}</h2>
      {note ? <p className="note">{note}</p> : null}
    </section>
  );
}

const app = express();

app.get('/orders/summary', (req: Request, res: Response) => {
  const html = renderToStaticMarkup(
    <OrderSummary customer={String(req.query.customer ?? '')} note={req.query.note as string | undefined} />
  );
  res.send('<!doctype html>' + html);
});

export default app;
