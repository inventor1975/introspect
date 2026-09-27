import express from 'express';
import Mustache from 'mustache';

const app = express();
app.use(express.urlencoded({ extended: true }));

const view = '<div class="bio"><h3>{{name}}</h3><div>{{{bio}}}</div></div>';

app.post('/members/bio-preview', (req, res) => {
  const { name, bio } = req.body;
  res.send(Mustache.render(view, { name, bio }));
});

export default app;
