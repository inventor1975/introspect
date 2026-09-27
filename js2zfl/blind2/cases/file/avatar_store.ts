import express, { Request, Response } from 'express';
import { promises as fsp } from 'fs';

const router = express.Router();
const AVATAR_ROOT = '/var/app/avatars';

interface AvatarPayload {
  username: string;
  image: string;
}

router.put('/profile/avatar', express.json({ limit: '2mb' }), async (req: Request, res: Response) => {
  const payload = req.body as AvatarPayload;
  if (!payload.image || !payload.image.startsWith('data:image/png;base64,')) {
    return res.status(415).json({ error: 'png only' });
  }
  const bytes = Buffer.from(payload.image.slice('data:image/png;base64,'.length), 'base64');
  const destination = `${AVATAR_ROOT}/${payload.username}.png`;
  await fsp.writeFile(destination, bytes);
  res.status(201).json({ url: `/avatars/${payload.username}.png` });
});

export default router;
