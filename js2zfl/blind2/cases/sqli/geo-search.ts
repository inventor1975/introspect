import { Router, Request, Response } from 'express';
import { Sequelize, literal } from 'sequelize';

const router = Router();
const sequelize = new Sequelize(process.env.DB_URL as string);
const Place = sequelize.define('Place', {});

router.get('/places/near', async (req: Request, res: Response) => {
  const radius = req.query.radius as string;
  const places = await Place.findAll({
    where: literal('distance < ' + radius),
    limit: 50,
  });
  res.json(places);
});

export default router;
