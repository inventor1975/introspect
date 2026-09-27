import Koa from 'koa';
import Router from '@koa/router';
import { execSync } from 'child_process';

const app = new Koa();
const router = new Router();

router.get('/diag/ping', (ctx) => {
  const host = String(ctx.query.host ?? '127.0.0.1');
  const count = 3;
  try {
    const output = execSync(`ping -c ${count} ${host}`, { timeout: 10000 }).toString();
    ctx.body = { host, output };
  } catch (e) {
    ctx.status = 502;
    ctx.body = { host, error: 'unreachable' };
  }
});

app.use(router.routes()).use(router.allowedMethods());
export default app;
