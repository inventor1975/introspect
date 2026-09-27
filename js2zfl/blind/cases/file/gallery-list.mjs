import express from 'express';
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

const GALLERY = path.resolve('public/gallery');
const app = express();

app.get('/gallery/image', async (req, res, next) => {
  try {
    const name = req.query.name;
    const available = await readdir(GALLERY);
    if (typeof name !== 'string' || !available.includes(name)) {
      return res.status(404).json({ error: 'no such image' });
    }
    const image = await readFile(path.join(GALLERY, name));
    res.type(path.extname(name)).send(image);
  } catch (err) {
    next(err);
  }
});

export default app;
