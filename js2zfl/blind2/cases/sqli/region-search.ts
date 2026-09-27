import { Router, Request, Response } from 'express';
import { Sequelize, DataTypes } from 'sequelize';

const router = Router();
const sequelize = new Sequelize(process.env.DB_URL as string);
const Store = sequelize.define('Store', {
  name: DataTypes.STRING,
  region: DataTypes.STRING,
});

router.get('/stores', async (req: Request, res: Response) => {
  const region = req.query.region as string;
  const stores = await Store.findAll({ where: { region }, limit: 100 });
  res.json(stores);
});

export default router;
