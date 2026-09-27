const express = require('express');
const crypto = require('crypto');
const fs = require('fs/promises');
const path = require('path');
const { Pool } = require('pg');

const pool = new Pool();
const BLOB_STORE = '/var/lib/intake/blobs';
const SHARED_DIR = '/var/lib/intake/shared';

const router = express.Router();

router.post('/intake', express.raw({ type: '*/*', limit: '20mb' }), async (req, res) => {
  const id = crypto.randomUUID();
  await fs.writeFile(path.join(BLOB_STORE, id), req.body);
  await pool.query('INSERT INTO intake_files (id, original_name) VALUES ($1, $2)', [
    id,
    req.get('X-File-Name') || 'unnamed.bin',
  ]);
  res.status(201).json({ id });
});

router.post('/intake/:id/publish', async (req, res) => {
  const { rows } = await pool.query('SELECT id, original_name FROM intake_files WHERE id = $1', [req.params.id]);
  if (rows.length === 0) {
    return res.sendStatus(404);
  }
  const record = rows[0];
  await fs.copyFile(path.join(BLOB_STORE, record.id), path.join(SHARED_DIR, record.original_name));
  res.json({ published: record.original_name });
});

module.exports = router;
