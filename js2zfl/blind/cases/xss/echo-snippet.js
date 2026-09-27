const Koa = require('koa');

const app = new Koa();

app.use(async (ctx, next) => {
  if (ctx.path !== '/snippet') return next();
  const snippet = ctx.query.content;
  ctx.status = 200;
  ctx.body = snippet;
});

app.listen(8080);
