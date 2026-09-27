import express, { Request, Response } from 'express';
import { encodeEntities } from './lib/entities';

const router = express.Router();

router.get('/team', (req: Request, res: Response) => {
  const department = encodeEntities(req.query.department);
  const role = encodeEntities(req.query.role);
  res.send(`<h2>${department}</h2><input type="hidden" name="role" value="${role}"><div id="people"></div>`);
});

export default router;
