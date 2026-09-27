import { Router } from 'express';
import { promises as fsp } from 'fs';
import path from 'path';

const ATTACH_DIR = path.resolve(__dirname, '../data/attachments');

const router = Router();

router.delete('/tickets/:ticketId/attachments/:id', async (req, res, next) => {
  try {
    const target = path.resolve(ATTACH_DIR, req.params.ticketId, req.params.id);
    await fsp.unlink(target);
    res.status(204).end();
  } catch (err: any) {
    if (err.code === 'ENOENT') {
      res.status(404).json({ error: 'attachment not found' });
      return;
    }
    next(err);
  }
});

export default router;
