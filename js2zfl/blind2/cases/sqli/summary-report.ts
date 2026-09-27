import { Router, Request, Response } from 'express';
import { Sequelize, QueryTypes } from 'sequelize';

const router = Router();
const sequelize = new Sequelize(process.env.DB_URL as string);

router.get('/reports/summary', async (req: Request, res: Response) => {
  const dept = req.query.dept as string;
  const rows = await sequelize.query(
    'SELECT dept, COUNT(*) AS n FROM employees WHERE dept = :dept GROUP BY dept',
    { replacements: { dept }, type: QueryTypes.SELECT }
  );
  res.json(rows);
});

export default router;
