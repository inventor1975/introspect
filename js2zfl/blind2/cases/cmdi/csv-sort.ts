import express from 'express';
import { execSync } from 'child_process';

const app = express();
app.use(express.json({ limit: '2mb' }));

app.post('/csv/sort', (req, res) => {
  const rows: string[] = Array.isArray(req.body.rows) ? req.body.rows : [];
  const numeric = req.body.numeric === true;
  const sorted = execSync(numeric ? 'sort -n -t, -k1,1' : 'sort -t, -k1,1', {
    input: rows.join('\n') + '\n',
    encoding: 'utf8',
  });
  res.json({ rows: sorted.trim().split('\n') });
});

export default app;
