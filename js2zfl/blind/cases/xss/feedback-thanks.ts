import Koa, { Context } from 'koa';
import Router from '@koa/router';
import bodyParser from 'koa-bodyparser';

interface FeedbackForm {
  email?: string;
  subject?: string;
}

const app = new Koa();
const router = new Router();

router.post('/feedback', async (ctx: Context) => {
  const form = ctx.request.body as FeedbackForm;
  const subject = form.subject || '(no subject)';
  ctx.type = 'html';
  ctx.body = `<p>Thanks! We received your message about <b>${subject}</b>.</p>`;
});

app.use(bodyParser());
app.use(router.routes());

export default app;
