import express from 'express';
import Mustache from 'mustache';

const app = express();
app.use(express.urlencoded({ extended: true }));

const view = `
<div class="speaker">
  <h3>{{name}}</h3>
  <p class="talk">{{talk}}</p>
  <div class="bio">{{bio}}</div>
</div>`;

app.post('/speakers/preview', (req, res) => {
  const { name, talk, bio } = req.body;
  res.send(Mustache.render(view, { name, talk, bio }));
});

export default app;
