import Koa from 'koa';
import Router from '@koa/router';
import { execSync } from 'child_process';

const ALLOWED_HOSTS = ['db-primary', 'db-replica', 'cache-01', 'cache-02', 'queue'];

const router = new Router();

router.get('/diag/reachability', (ctx) => {
  const host = String(ctx.query.host ?? '');
  if (!ALLOWED_HOSTS.includes(host)) {
    ctx.status = 400;
    ctx.body = { error: `unknown host ${host}` };
    return;
  }
  try {
    const output = execSync(`ping -c 2 -W 1 ${host}`).toString();
    ctx.body = { host, output };
  } catch {
    ctx.status = 502;
    ctx.body = { host, reachable: false };
  }
});

const app = new Koa();
app.use(router.routes());
export default app;
