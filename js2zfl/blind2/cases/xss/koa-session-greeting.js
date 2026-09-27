const Koa = require('koa');
const Router = require('@koa/router');

const app = new Koa();
const router = new Router();

app.use(async (ctx, next) => {
  ctx.state.visitor = ctx.query.as || ctx.cookies.get('visitor') || 'friend';
  await next();
});

router.get('/home', async (ctx) => {
  ctx.type = 'html';
  ctx.body = `<header>Hi there, ${ctx.state.visitor}</header>`;
});

app.use(router.routes());

module.exports = app;
