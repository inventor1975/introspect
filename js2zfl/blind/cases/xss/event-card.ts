import express, { Request, Response } from 'express';
import Handlebars from 'handlebars';

const app = express();

const card = Handlebars.compile<{ title: string; venue: string; when: string }>(`
  <article class="event">
    <h3>{{title}}</h3>
    <p class="venue">{{venue}}</p>
    <time>{{when}}</time>
  </article>`);

app.get('/events/card', (req: Request, res: Response) => {
  res.send(
    card({
      title: String(req.query.title || 'Untitled'),
      venue: String(req.query.venue || 'TBA'),
      when: String(req.query.when || ''),
    })
  );
});

export default app;
