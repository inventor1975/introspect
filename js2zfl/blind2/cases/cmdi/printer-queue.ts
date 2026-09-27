import Koa, { Context } from 'koa';
import Router from '@koa/router';
import { exec } from 'child_process';
import { requireQueueName } from './lib/validate';

const router = new Router();

router.get('/printers/:queue/jobs', async (ctx: Context) => {
  const queue = requireQueueName(ctx.params.queue);
  ctx.body = await new Promise<string[]>((resolve) => {
    exec(`lpstat -o ${queue}`, (err, stdout) => resolve(err ? [] : stdout.trim().split('\n')));
  });
});

const app = new Koa();
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (e: any) {
    ctx.status = e.status || 500;
    ctx.body = { error: e.message };
  }
});
app.use(router.routes());
export default app;
