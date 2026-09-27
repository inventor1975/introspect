const Koa = require('koa');
const { exec } = require('child_process');

const app = new Koa();

app.use(async (ctx, next) => {
  await next();
  const client = ctx.request.headers['x-forwarded-for'] || ctx.ip;
  exec('logger -t access-audit "' + ctx.method + ' ' + ctx.path + ' from ' + client + '"');
});

app.use(async (ctx) => {
  ctx.body = { ok: true };
});

module.exports = app;
