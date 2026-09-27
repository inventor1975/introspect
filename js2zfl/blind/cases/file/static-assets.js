const Koa = require('koa');
const send = require('koa-send');
const path = require('path');

const ASSETS = path.join(__dirname, 'assets');
const app = new Koa();

app.use(async (ctx, next) => {
  if (ctx.method !== 'GET' || !ctx.path.startsWith('/assets/')) return next();
  const rel = ctx.path.slice('/assets/'.length);
  await send(ctx, rel, { root: ASSETS, maxage: 86400000, immutable: true });
});

module.exports = app;
