import express from 'express';
import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';

const FEEDBACK_DIR = path.resolve('var/feedback');
const app = express();
app.use(express.json());

app.post('/feedback', async (req, res) => {
  const { subject, message, email } = req.body;
  if (!message) {
    return res.status(400).json({ error: 'message required' });
  }
  const id = randomUUID();
  const record = JSON.stringify({ id, subject, message, email, at: new Date().toISOString() });
  await writeFile(path.join(FEEDBACK_DIR, `${id}.json`), record, 'utf8');
  res.status(201).json({ id, subject });
});

export default app;
