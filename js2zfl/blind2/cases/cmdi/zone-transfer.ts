import { Request, Response, Router } from 'express';
import { exec } from 'child_process';

const router = Router();
const MAX_ZONE_LENGTH = 64;

router.post('/dns/axfr', (req: Request, res: Response) => {
  const zone: string = req.body.zone;
  if (typeof zone !== 'string' || zone.length === 0 || zone.length > MAX_ZONE_LENGTH) {
    res.status(400).send('invalid zone');
    return;
  }
  exec(`dig axfr ${zone} @ns1.internal`, (err, stdout) => {
    res.status(err ? 502 : 200).type('text').send(stdout);
  });
});

export default router;
