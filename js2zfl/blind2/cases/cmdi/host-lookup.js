const Koa = require('koa');
const Router = require('koa-router');
const { exec } = require('child_process');

const router = new Router();
const HOSTNAME_RE = /^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$/i;

router.get('/lookup/:host', async (ctx) => {
  const host = ctx.params.host;
  if (!HOSTNAME_RE.test(host)) {
    ctx.throw(400, 'invalid hostname');
  }
  ctx.body = await new Promise((resolve) => {
    exec(`host -W 2 ${host}`, (err, stdout) => resolve({ host, records: err ? [] : stdout.trim().split('\n') }));
  });
});

const app = new Koa();
app.use(router.routes());
module.exports = app;
