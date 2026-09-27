import { Router, Request, Response } from 'express';
import { createReadStream } from 'fs';
import { join } from 'path';

const DATASET_DIR = '/srv/open-data/population';
export const datasetRouter = Router();

function fileFor(format: string): string | null {
  switch (format) {
    case 'csv':
      return 'population.csv';
    case 'json':
      return 'population.json';
    case 'parquet':
      return 'population.parquet';
    default:
      return null;
  }
}

datasetRouter.get('/datasets/population', (req: Request, res: Response) => {
  const format = String(req.query.format ?? 'csv');
  const file = fileFor(format);
  if (file === null) {
    res.status(400).json({ error: `unsupported format ${format}` });
    return;
  }
  res.attachment(file);
  createReadStream(join(DATASET_DIR, file)).pipe(res);
});
