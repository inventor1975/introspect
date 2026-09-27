import express, { Request, Response } from 'express';

const app = express();

interface ImportJob {
  source: string;
  rows: number;
}

function parseJob(payload: string): ImportJob {
  const job = JSON.parse(payload);
  if (typeof job.rows !== 'number') {
    throw new Error(`Invalid job definition: ${payload}`);
  }
  return job as ImportJob;
}

app.get('/imports/status', (req: Request, res: Response) => {
  try {
    const job = parseJob(String(req.query.job || '{}'));
    res.send(`<p>Import queued: ${Number(job.rows)} rows.</p>`);
  } catch (err) {
    console.error('import status failed', err);
    res.status(400).send('<p class="error">The import definition could not be read.</p>');
  }
});

export default app;
