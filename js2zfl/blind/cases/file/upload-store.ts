import express, { Request, Response } from 'express';
import multer from 'multer';
import { randomUUID } from 'node:crypto';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';

const STORE = path.resolve(__dirname, '../uploads');
const EXT_BY_MIME: Record<string, string> = {
  'image/png': '.png',
  'image/jpeg': '.jpg',
  'application/pdf': '.pdf',
};

const upload = multer({ storage: multer.memoryStorage() });
export const uploads = express.Router();

uploads.post('/uploads', upload.single('file'), async (req: Request, res: Response) => {
  const file = req.file;
  if (!file) {
    res.status(400).json({ error: 'file required' });
    return;
  }
  const ext = EXT_BY_MIME[file.mimetype];
  if (!ext) {
    res.status(415).json({ error: `unsupported type ${file.mimetype}` });
    return;
  }
  const id = randomUUID();
  const label = String(req.body.label ?? file.originalname);
  await writeFile(path.join(STORE, id + ext), file.buffer);
  res.status(201).json({ id, label, original: file.originalname });
});
