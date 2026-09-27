const Koa = require('koa');
const Router = require('@koa/router');
const { exec } = require('child_process');

const router = new Router();

router.get('/disk', async (ctx) => {
  const human = ctx.query.human === 'true';
  const inodes = ctx.query.inodes === '1';
  const flags = [human ? '-h' : '-k', inodes ? '-i' : ''].join(' ').trim();
  ctx.body = await new Promise((resolve, reject) => {
    exec(`df ${flags} --local`, (err, stdout) => (err ? reject(err) : resolve(stdout)));
  });
  ctx.type = 'text/plain';
});

const app = new Koa();
app.use(router.routes());
module.exports = app;
