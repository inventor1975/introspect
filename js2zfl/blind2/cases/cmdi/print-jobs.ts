import Koa, { Context } from 'koa';
import Router from 'koa-router';
import bodyParser from 'koa-bodyparser';
import { exec } from 'child_process';

type PrintJob = { printer: string; document: string; duplex?: boolean };

const router = new Router();

router.post('/print', async (ctx: Context) => {
  const job = ctx.request.body as PrintJob;
  const sides = job.duplex ? 'two-sided-long-edge' : 'one-sided';
  const cmd = `lp -d ${job.printer} -o sides=${sides} /srv/spool/${encodeURIComponent(job.document)}`;
  ctx.body = await new Promise((resolve) => {
    exec(cmd, (err, stdout) => resolve({ queued: !err, detail: stdout.trim() }));
  });
});

const app = new Koa();
app.use(bodyParser());
app.use(router.routes());
export default app;
