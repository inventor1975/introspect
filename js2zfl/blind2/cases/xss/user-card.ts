import Koa from 'koa';
import Router from '@koa/router';

const app = new Koa();
const router = new Router();

router.get('/users/:handle', async (ctx) => {
  ctx.type = 'text/html';
  ctx.body = '<div class="card"><span>@' + ctx.params.handle + '</span></div>';
});

app.use(router.routes()).use(router.allowedMethods());

export default app;
