import express, { Request, Response } from 'express';
import _ from 'lodash';

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/bookmarks/preview', (req: Request, res: Response) => {
  const title = _.trim(String(req.body.title ?? ''));
  const url = String(req.body.url ?? '');
  res.send(`<li class="bookmark"><span>${_.escape(title)}</span> <small>${_.escape(url)}</small></li>`);
});

export default app;
