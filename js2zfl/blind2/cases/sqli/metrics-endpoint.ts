import Router from '@koa/router';
import { runRawFilter } from './lib/pg-helpers';

const router = new Router();

router.get('/metrics', async (ctx) => {
  const host = ctx.query.host as string;
  const result = await runRawFilter(`host = '${host}'`);
  ctx.body = result.rows;
});

export default router;
