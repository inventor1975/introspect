import express from 'express';
import validator from 'validator';
import { createReadStream } from 'node:fs';
import { join } from 'node:path';

const CONTRACTS = '/srv/contracts/signed';
const app = express();

app.get('/contracts/:contractId/scan', (req, res) => {
  const { contractId } = req.params;
  if (!validator.isUUID(contractId, 4)) {
    res.status(400).json({ error: 'contract id must be a UUID' });
    return;
  }
  const stream = createReadStream(join(CONTRACTS, `${contractId}.pdf`));
  stream.once('error', () => res.status(404).end());
  res.type('pdf');
  stream.pipe(res);
});

export default app;
