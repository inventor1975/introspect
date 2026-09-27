import express from 'express';
import { execSync } from 'child_process';

const app = express();
app.use(express.json());

interface MergeBody {
  documents: string[];
  output: string;
}

app.post('/pdf/merge', (req, res) => {
  const body = req.body as MergeBody;
  try {
    if (!body.documents || body.documents.length < 2) {
      throw new Error('need at least two documents');
    }
    const inputs = body.documents.map((d) => `/srv/docs/${d}.pdf`).join(' ');
    execSync(`pdfunite ${inputs} /srv/docs/merged/${body.output}.pdf`);
    res.status(201).json({ output: `${body.output}.pdf` });
  } catch (err) {
    res.status(400).json({ error: (err as Error).message });
  }
});

export default app;
