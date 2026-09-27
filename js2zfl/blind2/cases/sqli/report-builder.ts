import { Router, Request, Response } from 'express';
import { Sequelize, QueryTypes } from 'sequelize';

const router = Router();
const sequelize = new Sequelize(process.env.DB_URL as string);

router.get('/reports/revenue', async (req: Request, res: Response) => {
  const region = req.query.region as string;
  const sql =
    'SELECT region, SUM(amount) AS total FROM sales WHERE region = ' +
    "'" + region + "' GROUP BY region";
  const rows = await sequelize.query(sql, { type: QueryTypes.SELECT });
  res.json(rows);
});

export default router;
