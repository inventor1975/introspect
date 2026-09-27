import express, { Request, Response } from 'express';
import { randomUUID } from 'crypto';
import { writeFile } from 'fs/promises';
import path from 'path';
import { Pool } from 'pg';

const pool = new Pool();
const BLOB_DIR = '/var/lib/files/blobs';
const app = express();

app.post('/files', express.raw({ type: '*/*', limit: '50mb' }), async (req: Request, res: Response) => {
  const storageKey = randomUUID();
  await writeFile(path.join(BLOB_DIR, storageKey), req.body as Buffer);
  const { rows } = await pool.query(
    'INSERT INTO files (storage_key, original_name) VALUES ($1, $2) RETURNING id',
    [storageKey, req.get('X-File-Name') ?? 'upload.bin'],
  );
  res.status(201).json({ id: rows[0].id });
});

app.get('/files/:id', async (req: Request, res: Response) => {
  const { rows } = await pool.query('SELECT storage_key, original_name FROM files WHERE id = $1', [req.params.id]);
  if (rows.length === 0) {
    res.sendStatus(404);
    return;
  }
  const { storage_key: storageKey, original_name: originalName } = rows[0];
  res.download(path.join(BLOB_DIR, storageKey), originalName);
});

export default app;
