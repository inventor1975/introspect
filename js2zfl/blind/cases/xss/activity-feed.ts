import express, { Request, Response } from 'express';
import escape from 'lodash/escape';

const app = express();

type Activity = { actor: string; verb: string };

app.get('/activity', (req: Request, res: Response) => {
  const actor = String(req.query.actor || 'someone');
  const verbs = String(req.query.verbs || 'joined').split(',');
  const items: Activity[] = verbs.map((verb) => ({ actor, verb }));
  const html = items
    .map((a) => '<li>' + escape(a.actor) + ' ' + escape(a.verb) + '</li>')
    .join('');
  res.send('<ul class="feed">' + html + '</ul>');
});

export default app;
