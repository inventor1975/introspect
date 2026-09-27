import express, { Request, Response } from 'express';

const app = express();

const CITIES = ['Amsterdam', 'Berlin', 'Lisbon', 'Madrid', 'Oslo', 'Paris'];

app.get('/api/cities', (req: Request, res: Response) => {
  const prefix = String(req.query.prefix || '');
  const matches = CITIES.filter((c) => c.toLowerCase().startsWith(prefix.toLowerCase()));
  res.send({ prefix, matches, message: `<b>${matches.length}</b> results for ${prefix}` });
});

export default app;
