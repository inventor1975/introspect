import Koa from 'koa';
import Router from '@koa/router';
import { spawn } from 'child_process';

const router = new Router();

router.post('/transcode/:id', async (ctx) => {
  const preset = ctx.query.preset ?? 'medium';
  const bitrate = ctx.query.bitrate ?? '128k';
  const input = `/srv/audio/${Number(ctx.params.id)}.wav`;
  const script = `ffmpeg -y -i ${input} -preset ${preset} -b:a ${bitrate} ${input}.mp3`;
  const child = spawn('bash', ['-c', script], { stdio: 'ignore' });
  ctx.status = 202;
  ctx.body = { pid: child.pid };
});

const app = new Koa();
app.use(router.routes());
export default app;
