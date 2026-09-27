import express, { Request, Response } from 'express';
import multer from 'multer';
import * as fs from 'node:fs';
import * as path from 'node:path';

const AVATARS = path.resolve(process.cwd(), 'public', 'avatars');
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 2 * 1024 * 1024 } });

export const avatarRouter = express.Router();

avatarRouter.post('/me/avatar', upload.single('avatar'), async (req: Request, res: Response) => {
  if (!req.file) {
    res.status(400).json({ error: 'missing file' });
    return;
  }
  const filename: string = req.body.filename || req.file.originalname;
  const target = path.join(AVATARS, filename);
  await fs.promises.writeFile(target, req.file.buffer);
  res.status(201).json({ url: `/avatars/${encodeURIComponent(filename)}` });
});
