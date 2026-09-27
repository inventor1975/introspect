const Koa = require('koa');

const app = new Koa();

app.use(async (ctx, next) => {
  if (ctx.path !== '/bio') {
    return next();
  }
  const bio = ctx.query.bio;
  ctx.type = 'html';
  ctx.body = `<section class="bio"><p>${bio}</p></section>`;
});

app.listen(3000);
