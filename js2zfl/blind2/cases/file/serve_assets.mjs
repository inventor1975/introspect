import Koa from 'koa';
import Router from '@koa/router';
import send from 'koa-send';
import path from 'node:path';

const STATIC_DIR = path.resolve('build', 'client');
const router = new Router();

router.get('/app/:asset(.*)', async (ctx) => {
  const asset = ctx.params.asset || 'index.html';
  await send(ctx, asset, { root: STATIC_DIR, maxage: 86400000, immutable: true });
});

const app = new Koa();
app.use(router.routes());
export default app;
