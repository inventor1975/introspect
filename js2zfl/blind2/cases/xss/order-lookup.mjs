import express from 'express';
import { setTimeout as delay } from 'node:timers/promises';

const app = express();

async function lookupOrder(ref) {
  await delay(5);
  return ref === 'A-1000' ? { ref, total: 42 } : null;
}

app.get('/orders/find', async (req, res) => {
  const ref = req.query.ref;
  const order = await lookupOrder(ref);
  if (!order) {
    res.status(404).send(`<p>No order with reference <b>${ref}</b> was found.</p>`);
    return;
  }
  res.send(`<p>Order total: ${order.total}</p>`);
});

export default app;
