const Koa = require('koa');
const Router = require('koa-router');
const { execFile } = require('child_process');
const { promisify } = require('util');

const execFileAsync = promisify(execFile);
const router = new Router({ prefix: '/tools' });

router.get('/dig', async (ctx) => {
  const domain = ctx.query.domain;
  const type = ctx.query.type || 'A';
  const { stdout } = await execFileAsync('/bin/sh', ['-c', `dig +short ${type} ${domain}`]);
  ctx.body = stdout.trim().split('\n');
});

const app = new Koa();
app.use(router.routes());
module.exports = app;
