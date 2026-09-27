import Koa, { Context } from 'koa';
import Router from '@koa/router';

const app = new Koa();
const router = new Router();

router.get('/export/preview', async (ctx: Context) => {
  const columns = String(ctx.query.columns || 'id,name').split(',');
  const header = columns.map((c) => c.trim()).join(';');
  ctx.type = 'text/plain';
  ctx.body = `<export>\n${header}\n`;
});

app.use(router.routes());

export default app;
