import express, { Request, Response } from 'express';
import { readFile } from 'fs/promises';
import path from 'path';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

const AVATARS = path.join(__dirname, 'avatars');
const OBJECT_ID = /^[a-f0-9]{24}$/;

const AvatarCard: React.FC<{ id: string; dataUri: string }> = ({ id, dataUri }) => (
  <figure>
    <img src={dataUri} alt={`avatar ${id}`} />
  </figure>
);

const router = express.Router();

router.get('/users/:userId/avatar-card', async (req: Request, res: Response) => {
  const userId = req.params.userId.toLowerCase();
  if (!OBJECT_ID.test(userId)) {
    res.status(400).send('bad user id');
    return;
  }
  const png = await readFile(path.join(AVATARS, `${userId}.png`));
  const html = renderToStaticMarkup(<AvatarCard id={userId} dataUri={`data:image/png;base64,${png.toString('base64')}`} />);
  res.send(html);
});

export default router;
