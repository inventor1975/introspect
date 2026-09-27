import express, { Request, Response } from 'express';

const router = express.Router();

router.get('/hello/:name', (req: Request, res: Response) => {
  const { name } = req.params;
  res.status(200).send(`<!doctype html><title>Hi</title><p>Hello, ${name}!</p>`);
});

export default router;
