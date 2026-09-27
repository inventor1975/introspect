import Koa from 'koa';
import Router from '@koa/router';
import { createReadStream } from 'fs';
import { stat } from 'fs/promises';
import { join } from 'path';

const ATTACHMENTS = '/var/lib/support/attachments';
const NUMERIC = /^\d{1,12}$/;

const router = new Router();

router.get('/tickets/:ticket/attachments/:attachment', async (ctx: Koa.Context) => {
  const { ticket, attachment } = ctx.params;
  if (!NUMERIC.test(ticket) || !NUMERIC.test(attachment)) {
    ctx.throw(400, 'ids must be numeric');
  }
  const file = join(ATTACHMENTS, ticket, `${attachment}.bin`);
  const info = await stat(file).catch(() => null);
  if (!info) {
    ctx.throw(404);
  }
  ctx.length = info!.size;
  ctx.body = createReadStream(file);
});

const app = new Koa();
app.use(router.routes());
export default app;
