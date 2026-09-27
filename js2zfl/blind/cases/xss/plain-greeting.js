const Koa = require('koa');
const Router = require('@koa/router');

const app = new Koa();
const router = new Router();

router.get('/greet', (ctx) => {
  const name = ctx.query.name || 'stranger';
  ctx.body = `Hello, ${name}! Nice to see you.`;
});

app.use(router.routes());

module.exports = app;
