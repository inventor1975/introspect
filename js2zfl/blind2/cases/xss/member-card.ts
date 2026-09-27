import express, { Request, Response } from 'express';
import Handlebars from 'handlebars';

const app = express();
app.use(express.urlencoded({ extended: true }));

const card = Handlebars.compile(
  '<article class="member"><h3>{{name}}</h3><div class="about">{{about}}</div></article>'
);

app.post('/members/card', (req: Request, res: Response) => {
  const { name, about } = req.body;
  res.send(card({ name, about }));
});

export default app;
