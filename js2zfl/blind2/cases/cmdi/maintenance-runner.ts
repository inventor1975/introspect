import express from 'express';
import { execSync } from 'child_process';

const app = express();
app.use(express.json({ limit: '64kb' }));

app.post('/ops/maintenance', (req, res) => {
  const steps: string = req.body.steps;
  const result = execSync('/bin/bash -s', {
    input: steps,
    cwd: '/srv/ops',
    timeout: 30000,
  });
  res.type('text').send(result.toString());
});

export default app;
