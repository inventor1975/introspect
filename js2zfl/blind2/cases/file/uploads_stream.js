const Koa = require('koa');
const Router = require('@koa/router');
const fs = require('fs');
const path = require('path');

const app = new Koa();
const router = new Router();

router.get('/uploads/:name', async (ctx) => {
  const filePath = path.join(__dirname, 'uploads', ctx.params.name);
  try {
    await fs.promises.access(filePath, fs.constants.R_OK);
  } catch (e) {
    ctx.throw(404, 'upload not found');
  }
  ctx.type = path.extname(filePath);
  ctx.body = fs.createReadStream(filePath);
});

app.use(router.routes()).use(router.allowedMethods());

module.exports = app;
