const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');
const escape = require('escape-html');

const app = new Koa();
const router = new Router();

router.post('/comments/preview', async (ctx) => {
  const { author, text } = ctx.request.body;
  ctx.type = 'html';
  ctx.body = `<blockquote><p>${escape(text)}</p><cite>${escape(author)}</cite></blockquote>`;
});

app.use(bodyParser());
app.use(router.routes());

module.exports = app;
