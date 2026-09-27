import express from 'express';
import pg from 'pg';

const router = express.Router();
const pool = new pg.Pool({ connectionString: process.env.PG_URL });

router.post('/feedback', async (req, res) => {
  const { subject, message } = req.body;
  const text =
    "INSERT INTO feedback (subject, message) VALUES ('" +
    subject + "', '" + message + "')";
  await pool.query(text);
  res.status(201).json({ ok: true });
});

export default router;
