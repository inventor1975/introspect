import express, { Request, Response } from 'express';

const app = express();

const CURRENCIES = new Set(['USD', 'EUR', 'GBP', 'JPY', 'CHF']);

app.get('/pricing', (req: Request, res: Response) => {
  let currency = String(req.query.currency || '').toUpperCase();
  if (!CURRENCIES.has(currency)) {
    currency = 'USD';
  }
  res.send(`<select name="currency"><option selected>${currency}</option></select><div id="plans" data-currency="${currency}"></div>`);
});

export default app;
