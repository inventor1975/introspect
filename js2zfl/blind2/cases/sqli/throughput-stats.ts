import Router from '@koa/router';
import { runBoundQuery } from './lib/pg-helpers';

const router = new Router();

router.get('/throughput', async (ctx) => {
  const host = ctx.query.host as string;
  const result = await runBoundQuery(
    'SELECT ts, value FROM metrics WHERE host = $1 ORDER BY ts DESC LIMIT 200',
    [host]
  );
  ctx.body = result.rows;
});

export default router;
