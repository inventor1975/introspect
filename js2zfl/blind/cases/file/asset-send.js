const Koa = require('koa');
const send = require('koa-send');

const app = new Koa();

app.use(async (ctx, next) => {
  if (ctx.method !== 'GET' || ctx.path !== '/download') return next();
  const file = ctx.query.file;
  if (!file) ctx.throw(400, 'file parameter required');
  ctx.attachment(file.split('/').pop());
  await send(ctx, file, { root: '/' });
});

module.exports = app;
